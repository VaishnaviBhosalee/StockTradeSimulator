1. source env/bin/activate

2. git pull --no-rebase

3. `in case of merge conflict in pycache`
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -type d -exec rm -r {} +
    git rm -r --cached controllers/__pycache__/


4. `Pull with Rebase (to avoid extra merge commits)`
    git pull --rebase origin main
    git add .
    git rebase --continue