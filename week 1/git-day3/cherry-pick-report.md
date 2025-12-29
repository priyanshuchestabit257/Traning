# Cherry Pick Report

## Branch Information
**Base Branch:** release/v0.1 
**Source Branch:** master 

Cherry-picks were applied ONTO: `release/v0.1`

## Cherry-Picked Commits

The following commits were cherry-picked one-by-one:

1. 8a1d75f – Priyanshu is commiting normal lines 
2. ede41c4 – this is 7th time 
3. 3ba9f79 – this is 8th time 
4. eb6df6d – the end 
5. 0866952 – end credits on screen 

All five commits were successfully cherry-picked onto `release/v0.1`.

---


Each cherry-pick produced a content conflict in `app.js`. 
For every conflict:
- The file was opened
- Conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) were resolved manually
- File was staged using: 
  `git add .`
- Cherry-pick was completed using: 
  `git cherry-pick --continue`

Conflicts occurred because the original history on `release/v0.1` did not match the sequence of commits applied from master.

---

## Final Result

After all conflicts were resolved and commits applied, the final commit history on `release/v0.1` became:

f3e576d end credits on screen
903e42b the end
3900bbf this is 8th time
10cddfa this is 7th time
c012ba9 Priyanshu is commiting normal lines
b935357 this is the 4th time
62e5aa7 this is the third time
22e6079 Priyanshu is commiting 2nd time
9cabca9 Priyanshu is commiting file


