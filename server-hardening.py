import subprocess

def run(cmd, check=True):
    print(f">>> {cmd}")
    subprocess.run(cmd, shell=True, check=check)

def harden_server():
    # 1. Install and configure UFW
    run("sudo apt update && sudo apt upgrade -y")
    run("sudo apt install ufw -y")
    run("sudo ufw logging on")

    # 2. Allow both SSH ports for now
    run("sudo ufw allow 22/tcp")    # current connection
    run("sudo ufw allow 2222/tcp")  # future connection

    # 3. Configure SSH to listen on 2222
    run("sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup")
    run("sudo sed -i 's/^#Port 22/Port 2222/' /etc/ssh/sshd_config")
    run("sudo sed -i 's/^Port 22/Port 2222/' /etc/ssh/sshd_config")

    # 4. Restart SSH
    run("sudo systemctl restart ssh")

    # 5. Enable UFW
    run("sudo ufw --force enable")

    print("\n✅ SSH now listens on both ports 22 and 2222.")
    print("👉 Please test SSH access via port 2222 before locking down port 22.")

if __name__ == "__main__":
    harden_server()
