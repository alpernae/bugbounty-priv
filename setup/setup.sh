#!/bin/bash
set -e

# Color output for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[*]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[x]${NC} $1"
}

# Check if running as root for sudo commands
if [[ $EUID -ne 0 ]]; then
   log_error "This script must be run with sudo privileges"
   exit 1
fi

log_info "Starting BlackBox Automation setup..."

# ============================================
# SECTION 1: System Dependencies
# ============================================
log_info "Updating system and installing dependencies..."
apt update && apt upgrade -y
apt install -y build-essential git curl wget nano golang python3 python3-pip nodejs npm nmap ffuf

# ============================================
# SECTION 2: Project Discovery Tools
# ============================================
log_info "Installing ProjectDiscovery tools via pdtm..."
go install -v github.com/projectdiscovery/pdtm/cmd/pdtm@latest

PDTM_PATH="$HOME/go/bin/pdtm"
if [ -f "$PDTM_PATH" ]; then
    log_info "Running pdtm installer..."
    $PDTM_PATH -ia
    
    # Move tools to system PATH
    if [ -d "$HOME/.pdtm/go/bin" ]; then
        cp $HOME/.pdtm/go/bin/* /usr/local/bin/
        log_info "ProjectDiscovery tools installed successfully"
    fi
else
    log_error "pdtm not found at $PDTM_PATH"
fi

# ============================================
# SECTION 3: Individual Go Tools Installation
# ============================================
log_info "Installing additional Go-based tools..."

# Gungnir - Real-time certificate tracking
log_info "Installing gungnir..."
go install github.com/g0ldencybersec/gungnir/cmd/gungnir@latest
if [ -f "$HOME/go/bin/gungnir" ]; then
    cp $HOME/go/bin/gungnir /usr/local/bin/
    log_info "gungnir installed successfully"
else
    log_error "gungnir installation failed"
fi

# Notify - Unified notification tool for Discord, Slack, Telegram, etc.
log_info "Installing notify..."
go install -v github.com/projectdiscovery/notify/cmd/notify@latest
if [ -f "$HOME/go/bin/notify" ]; then
    cp $HOME/go/bin/notify /usr/local/bin/
    log_info "notify installed successfully"
else
    log_error "notify installation failed"
fi

# ============================================
# SECTION 4: MassDNS Installation
# ============================================
log_info "Installing massdns..."
MASSDNS_DIR="/usr/share/massdns"

if [ ! -d "$MASSDNS_DIR" ]; then
    cd /usr/share
    git clone https://github.com/blechschmidt/massdns
    cd massdns
    make
    cp bin/massdns /usr/local/bin/
    log_info "massdns installed successfully"
else
    log_warn "massdns already exists at $MASSDNS_DIR"
fi

# ============================================
# SECTION 5: Wordlists Setup
# ============================================
log_info "Setting up wordlists directory..."
WORDLIST_DIR="$HOME/wordlists"
mkdir -p "$WORDLIST_DIR"
cd "$WORDLIST_DIR"

# SecLists
if [ ! -d "SecLists" ]; then
    log_info "Cloning SecLists..."
    git clone https://github.com/danielmiessler/SecLists
    log_info "SecLists installed"
else
    log_warn "SecLists already exists"
fi

# Assetnote Wordlists
if [ ! -d "assetnote" ]; then
    log_info "Downloading Assetnote wordlists..."
    mkdir -p assetnote
    cd assetnote
    wget -r --no-parent -R "index.html*" https://wordlists-cdn.assetnote.io/data/ -nH -e robots=off -q
    cd "$WORDLIST_DIR"
    log_info "Assetnote wordlists installed"
else
    log_warn "Assetnote wordlists already exist"
fi

# ============================================
# SETUP COMPLETE
# ============================================
log_info "Setup completed successfully!"
log_info "Wordlists directory: $WORDLIST_DIR"
log_info "Tools installed in: /usr/local/bin/"