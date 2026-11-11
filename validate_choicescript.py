#!/usr/bin/env python3
"""ChoiceScript Syntax, Variable, Label, Flow, and Requirement Validator."""

import os
import re
import sys

SCENES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenes")

VALID_COMMANDS = {
    "title", "author", "scene_list", "create", "temp", "set",
    "if", "elseif", "else", "choice", "fake_choice", "selectable_if",
    "label", "goto", "goto_scene", "gosub", "gosub_scene", "return",
    "ending", "finish", "input_text", "stat_chart", "rand", "comment"
}


def validate_all():
    errors = []
    created_vars = set()
    scene_labels = {}
    scene_files = sorted(f for f in os.listdir(SCENES_DIR) if f.endswith(".txt"))

    # Pass 1: Collect *create variables from startup.txt and all *label declarations
    for fname in scene_files:
        sname = fname[:-4]
        scene_labels[sname] = set()
        fpath = os.path.join(SCENES_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            for lineno, raw_line in enumerate(f, 1):
                line = raw_line.rstrip("\r\n")
                stripped = line.lstrip(" ")
                if stripped.startswith("*create "):
                    parts = stripped.split(None, 2)
                    if len(parts) < 3:
                        errors.append(f"{fname}:{lineno}: Invalid *create syntax: {stripped}")
                    else:
                        created_vars.add(parts[1])
                elif stripped.startswith("*label "):
                    parts = stripped.split()
                    if len(parts) != 2:
                        errors.append(f"{fname}:{lineno}: Invalid *label syntax: {stripped}")
                    else:
                        lbl = parts[1]
                        if lbl in scene_labels[sname]:
                            errors.append(f"{fname}:{lineno}: Duplicate label '{lbl}'")
                        scene_labels[sname].add(lbl)

    # Pass 2: Validate commands, indentation, variables, labels, and sensory word counts
    for fname in scene_files:
        sname = fname[:-4]
        fpath = os.path.join(SCENES_DIR, fname)
        temp_vars = set()
        with open(fpath, "r", encoding="utf-8") as f:
            lines = [l.rstrip("\r\n") for l in f]

        for lineno, line in enumerate(lines, 1):
            if "\t" in line:
                errors.append(f"{fname}:{lineno}: Tab character found (use spaces only)")
            stripped = line.lstrip(" ")
            if not stripped:
                continue
            indent = len(line) - len(stripped)
            if indent % 2 != 0:
                errors.append(f"{fname}:{lineno}: Odd indentation ({indent} spaces): {line}")

            # Check ChoiceScript commands
            if stripped.startswith("*"):
                cmd_part = stripped[1:].split(None, 1)[0]
                if cmd_part not in VALID_COMMANDS:
                    errors.append(f"{fname}:{lineno}: Unknown command '*{cmd_part}'")

                if cmd_part == "temp":
                    parts = stripped.split(None, 2)
                    if len(parts) >= 2:
                        temp_vars.add(parts[1])

                elif cmd_part == "set":
                    parts = stripped.split(None, 2)
                    if len(parts) < 3:
                        errors.append(f"{fname}:{lineno}: Invalid *set: {stripped}")
                    else:
                        vname = parts[1]
                        if vname not in created_vars and vname not in temp_vars:
                            errors.append(f"{fname}:{lineno}: Undeclared variable in *set: '{vname}'")

                elif cmd_part == "rand":
                    parts = stripped.split()
                    if len(parts) != 4:
                        errors.append(f"{fname}:{lineno}: Invalid *rand syntax: {stripped}")
                    elif parts[1] not in created_vars and parts[1] not in temp_vars:
                        errors.append(f"{fname}:{lineno}: Undeclared variable in *rand: '{parts[1]}'")

                elif cmd_part == "input_text":
                    parts = stripped.split()
                    if len(parts) != 2 or (parts[1] not in created_vars and parts[1] not in temp_vars):
                        errors.append(f"{fname}:{lineno}: Invalid *input_text: {stripped}")

                elif cmd_part in ("goto", "gosub"):
                    parts = stripped.split()
                    if len(parts) != 2:
                        errors.append(f"{fname}:{lineno}: Invalid *{cmd_part}: {stripped}")
                    elif parts[1] not in scene_labels[sname]:
                        errors.append(f"{fname}:{lineno}: Missing target label '{parts[1]}' in {fname}")

                elif cmd_part in ("goto_scene", "gosub_scene"):
                    parts = stripped.split()
                    if len(parts) < 2 or len(parts) > 3:
                        errors.append(f"{fname}:{lineno}: Invalid *{cmd_part}: {stripped}")
                    else:
                        target_scene = parts[1]
                        if target_scene not in scene_labels:
                            errors.append(f"{fname}:{lineno}: Unknown target scene '{target_scene}'")
                        elif len(parts) == 3 and parts[2] not in scene_labels[target_scene]:
                            errors.append(
                                f"{fname}:{lineno}: Unknown label '{parts[2]}' in scene '{target_scene}'"
                            )

                elif cmd_part in ("if", "elseif", "selectable_if"):
                    if cmd_part == "selectable_if":
                        cond_str = stripped.split("#", 1)[0][len("*selectable_if"):].strip()
                    else:
                        cond_str = stripped[len(cmd_part) + 1:].strip()
                    # Check all identifier tokens in condition
                    cond_no_strings = re.sub(r'"[^"]*"', '""', cond_str)
                    for tok in re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", cond_no_strings):
                        if tok in ("and", "or", "not", "true", "false"):
                            continue
                        if tok not in created_vars and tok not in temp_vars:
                            errors.append(
                                f"{fname}:{lineno}: Undeclared variable '{tok}' in *{cmd_part}: {cond_str}"
                            )

            # Check ${...} interpolations (must be a single valid variable name)
            for match in re.finditer(r"\$\{([^}]+)\}", stripped):
                expr = match.group(1).strip()
                if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", expr):
                    errors.append(
                        f"{fname}:{lineno}: Complex expression inside '${{{expr}}}' not allowed in ChoiceScript"
                    )
                elif expr not in created_vars and expr not in temp_vars:
                    errors.append(f"{fname}:{lineno}: Undeclared variable '${{{expr}}}'")

        # If district file, verify sensory description word count (150-250 words) and bolded places (>= 8)
        if fname.startswith("district_"):
            desc_lines = []
            in_desc = False
            for line in lines:
                s = line.strip()
                if s.startswith("*set ") and "_visits" in s:
                    in_desc = True
                    continue
                if in_desc:
                    if s.startswith("----"):
                        break
                    if not s.startswith("*"):
                        desc_lines.append(s)
            desc_text = " ".join(desc_lines).strip()
            bold_places = re.findall(r"\[b\]([^\[]+)\[/b\]", desc_text)
            clean_text = re.sub(r"\[/?[bi]\]", "", desc_text)
            words = clean_text.split()
            word_count = len(words)
            print(
                f"  [DISTRICT CHECK] {fname:30s} -> Sensory words: {word_count:3d} (req 150-250), Named [b] places in intro: {len(bold_places)}"
            )
            if not (150 <= word_count <= 250):
                errors.append(
                    f"{fname}: Sensory description word count is {word_count} (must be 150-250)"
                )
            if len(bold_places) < 8:
                errors.append(
                    f"{fname}: Only {len(bold_places)} named places in sensory intro (need >= 8)"
                )

    print(f"\nValidated {len(scene_files)} scene files and {len(created_vars)} global variables.")
    if errors:
        print("\nERRORS FOUND:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    else:
        print("ALL CHOICESCRIPT SYNTAX, VARIABLE, LABEL, AND REALISM CHECKS PASSED!")


if __name__ == "__main__":
    validate_all()
