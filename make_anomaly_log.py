lines = []

# Normal hours (08:00 to 17:00): only 3 failures per hour
for hour in range(8, 18):
    for minute in (10, 20, 30):
        lines.append(
            f"Oct 03 {hour:02d}:{minute:02d}:00 server sshd[1]: "
            f"Failed password for bob from 198.51.100.7 port 40000 ssh2"
        )

# Spike at 18:00: 60 failures in one hour
for minute in range(60):
    lines.append(
        f"Oct 03 18:{minute:02d}:00 server sshd[1]: "
        f"Failed password for root from 203.0.113.99 port 50000 ssh2"
    )

# Back to normal at 19:00
for minute in (10, 20, 30):
    lines.append(
        f"Oct 03 19:{minute:02d}:00 server sshd[1]: "
        f"Failed password for bob from 198.51.100.7 port 40000 ssh2"
    )

with open("examples/anomaly.log", "w") as file:
    file.write("\n".join(lines) + "\n")

print(f"Wrote {len(lines)} lines to examples/anomaly.log")