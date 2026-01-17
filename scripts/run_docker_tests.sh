#!/bin/bash

# Docker Test Runner Script for Flask 2 Boilerplate
# This script runs tests inside the Docker container

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
COVERAGE=false
VERBOSE=false
SPECIFIC_TEST=""
PYTEST_ARGS=""

# Function to display help
show_help() {
    cat << EOF
${BLUE}Flask 2 Boilerplate - Docker Test Runner${NC}

Usage: bash scripts/run_docker_tests.sh [options]

Options:
    -h, --help              Show this help message
    -c, --coverage          Run tests with coverage report
    -v, --verbose           Run tests with verbose output
    -t, --test TEST         Run specific test (e.g., test_authentication.py)
    -s, --stop-on-fail      Stop on first failure
    --lf, --last-failed     Run only last failed tests
    --ff, --failed-first    Run failed tests first
    --build                 Build containers before running tests
    --no-cleanup            Don't remove containers after tests

Examples:
    bash scripts/run_docker_tests.sh                    # Run all tests in container
    bash scripts/run_docker_tests.sh --coverage         # With coverage report
    bash scripts/run_docker_tests.sh -v                 # Verbose output
    bash scripts/run_docker_tests.sh -t test_authentication
    bash scripts/run_docker_tests.sh --build -c -v      # Build, then run with coverage

EOF
}

# Parse arguments
BUILD_CONTAINERS=false
NO_CLEANUP=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            PYTEST_ARGS="${PYTEST_ARGS} -v"
            shift
            ;;
        -t|--test)
            SPECIFIC_TEST="$2"
            shift 2
            ;;
        -s|--stop-on-fail|-x|--exitfirst)
            PYTEST_ARGS="${PYTEST_ARGS} -x"
            shift
            ;;
        --lf|--last-failed)
            PYTEST_ARGS="${PYTEST_ARGS} --lf"
            shift
            ;;
        --ff|--failed-first)
            PYTEST_ARGS="${PYTEST_ARGS} --ff"
            shift
            ;;
        --build)
            BUILD_CONTAINERS=true
            shift
            ;;
        --no-cleanup)
            NO_CLEANUP=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# Navigate to project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Flask 2 Boilerplate - Docker Test Runner${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Build containers if requested
if [ "$BUILD_CONTAINERS" = true ]; then
    echo -e "${BLUE}Building Docker containers...${NC}"
    docker-compose build
    echo ""
fi

# Check if Flask container is running
CONTAINER_RUNNING=$(docker-compose ps flask 2>/dev/null | grep -c "Up" || true)

if [ "$CONTAINER_RUNNING" -eq 0 ]; then
    echo -e "${YELLOW}Flask container not running. Starting it...${NC}"
    docker-compose up -d flask
    echo ""
    echo -e "${BLUE}Waiting for container to start...${NC}"
    
    # Countdown with visual progress
    for i in {15..1}; do
        if [ $i -gt 10 ]; then
            progress_color="${BLUE}"
        elif [ $i -gt 5 ]; then
            progress_color="${YELLOW}"
        else
            progress_color="${RED}"
        fi
        
        printf "\r${progress_color}Starting in: %2d seconds${NC} [" $i
        
        # Show progress bar
        filled=$((15 - i))
        empty=$((i))
        for ((j=0; j<filled; j++)); do printf "="; done
        for ((j=0; j<empty; j++)); do printf " "; done
        printf "]"
        
        sleep 1
    done
    printf "\r${GREEN}Container started!${NC}                                    \n"
    echo ""
fi

# Build the pytest command
PYTEST_CMD="pytest"

# Add coverage if requested
if [ "$COVERAGE" = true ]; then
    echo -e "${BLUE}Running tests with coverage report...${NC}"
    PYTEST_CMD="$PYTEST_CMD --cov=boilerplate tests/"
    PYTEST_ARGS="${PYTEST_ARGS} --cov-report=html --cov-report=term-missing"
else
    PYTEST_CMD="$PYTEST_CMD tests/"
fi

# Add specific test if provided
if [ -n "$SPECIFIC_TEST" ]; then
    echo -e "${BLUE}Running specific test: $SPECIFIC_TEST${NC}"
    PYTEST_CMD="$PYTEST_CMD/$SPECIFIC_TEST"
fi

# Add any additional pytest arguments
if [ -n "$PYTEST_ARGS" ]; then
    PYTEST_CMD="$PYTEST_CMD $PYTEST_ARGS"
fi

# Add default verbose flag if not already set
if [ "$VERBOSE" = false ]; then
    PYTEST_CMD="$PYTEST_CMD -v"
fi

echo -e "${BLUE}Running inside Docker container...${NC}"
echo -e "${BLUE}Command: $PYTEST_CMD${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Run pytest inside the container
if docker-compose exec -T flask bash -c "cd /deploy && $PYTEST_CMD"; then
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo -e "${BLUE}========================================${NC}"
    
    # Show coverage report info if coverage was run
    if [ "$COVERAGE" = true ]; then
        echo ""
        echo -e "${GREEN}Coverage report generated:${NC}"
        echo -e "  ${YELLOW}HTML Report: htmlcov/index.html${NC}"
    fi
    
    # Cleanup if not disabled
    if [ "$NO_CLEANUP" = false ]; then
        echo ""
        echo -e "${BLUE}Stopping containers...${NC}"
        docker-compose down
    fi
    
    exit 0
else
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${RED}✗ Some tests failed!${NC}"
    echo -e "${BLUE}========================================${NC}"
    
    # Cleanup if not disabled
    if [ "$NO_CLEANUP" = false ]; then
        echo ""
        echo -e "${BLUE}Stopping containers...${NC}"
        docker-compose down
    fi
    
    exit 1
fi
