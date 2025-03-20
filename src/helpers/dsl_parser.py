import re


def parse_dsl(dsl_script: str) -> list[dict]:
    """
    Extended DSL commands:
      SET var = value
      INCR var BY value
      IF var > value THEN [command]
    Each command is parsed into a dict describing its type & parameters.
    """
    lines = dsl_script.splitlines()
    commands = []
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # SET ...
        set_match = re.match(r"^SET\s+(\w+)\s*=\s*(\d+)$", line, re.IGNORECASE)
        if set_match:
            var, value = set_match.groups()
            commands.append({"type": "SET", "var": var, "value": int(value)})
            continue

        # INCR ...
        incr_match = re.match(r"^INCR\s+(\w+)\s+BY\s+(\d+)$", line, re.IGNORECASE)
        if incr_match:
            var, amount = incr_match.groups()
            commands.append({"type": "INCR", "var": var, "amount": int(amount)})
            continue

        # IF ... THEN ...
        if_match = re.match(r"^IF\s+(\w+)\s*>\s*(\d+)\s+THEN\s+(.*)$", line, re.IGNORECASE)
        if if_match:
            var, threshold, then_command = if_match.groups()
            commands.append({
                "type": "IF",
                "var": var,
                "op": ">",
                "value": int(threshold),
                "then": then_command.strip()
            })
            continue

        raise ValueError(f"Invalid DSL line: '{line}'")

    return commands
