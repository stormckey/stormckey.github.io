# Git Learning Notes

!!! abstract "一个自底向上的学习过程，最后附上了常用指令，暂无操作演示，可以参考原[课程网站](https://missing.csail.mit.edu/2020/version-control/)"
## Terminology

!!! info "定义"
    - 一个文件被称作**blob**.  
    - 一个文件夹被称作**tree**.  
    - 整个仓库的快照被称作**commit**.  
    - commit的有向无环图构成**history**. 
    - 一个**object**是blob、tree或者commit，没个对象都有自己对应的hash.
    - 一个**reference**是一个对象的别名，或者我们通过hash来引用一个对象.
    - **main/master** 作为一个特殊的reference总是指向开发中的最新稳定版本.
    - **HEAD** 作为一个特殊引用指向我们目前在历史中的何处.
    - 一个 **Git repository*** 是object和reference的集合.
    - **Staging area** 是一种机制来让我们指定哪些对象要被commit, 而非整个仓库.
## Git Data Model
首先定义数据对象
```
// a file is a bunch of bytes
type blob = array<byte>

// a directory contains named files and directories
type tree = map<string, tree | blob>

// a commit has parents, metadata, and the top-level tree
type commit = struct {
    parents: array<commit>
    author: string
    message: string
    snapshot: tree
}

//An object is a blob,tree,or commit
type object = blob | tree | commit
```  

在Git存储结构中，每个对象对应一个hash
```
objects = map<string, object>

def store(object):
    id = sha1(object)
    objects[id] = object

def load(id):
    return objects[id]
```
## Commands

!!! info "Basic"
    - `git help <command>` : get help for a git command
    - `git init` : creates a new git repo, with data stored in the .git directory
    - `git status` : tells you what’s going on
    - `git add <filename>` : adds files to staging area
    - `git commit` : creates a new commit
    - `git log` : shows a flattened log of history
    - `git log --all --graph --decorate` : visualizes history as a DAG
    - `git diff <filename>` : show the differences between current file and HEAD version file
    - `git diff <revision> <filename>` : shows differences between current file and specified snapshot
    - `git diff <reversin> <reversion> <filename>` shows the differences between two specified version of file
    - `git checkout <revision>` : updates HEAD and current branch
    - `git checkout <filename>` : erase all the changes we made after the HEAD version for this file
    - `git cat-file -p <hash>` : The instruction to catch a tree or blob
!!! info "Branching and Merging"
    - `git branch`: shows branches
    - `git branch <name>`: creates a branch
    - `git checkout -b <name>`: creates a branch and switches to it
      - same as `git branch <name>`; `git checkout <name>`
    - `git merge <revision>` : merges into current branch;wait for latter adjustments when conflictions occur(But the file has been changed already)
    - `git merge --abort` : erase the changes git try to make when an merge conflict occurs
    - `git merge --continue` : continue to merge after you fix the merge confliction
    - `git mergetool`: use a fancy tool to help resolve merge conflicts
    - `git rebase`: rebase set of patches onto a new base
!!! info "Remotes"
    - `git remote`: list remotes
    - `git remote add <name> <url>`: add a remote ;name is origin by convention if we have only one remote; url can be a web address or a local directory 
    - `git push <remote> <local branch>:<remote branch>`: send objects to remote, and update remote reference
    - `git branch --set-upstream-to=<remote>/<remote branch>`: set up correspondence between local and remote branch
    - `git fetch`: retrieve objects/references from a remote; be aware of the changes pushed here from the remote 
    - `git pull`: same as git fetch; git merge
    - `git clone`: download repository from remote
!!! info "Undo"
    - `git commit --amend`: edit a commit’s contents/message
    - `git reset HEAD <file>`: unstage a file
    - `git checkout <file>`: discard changes
!!! info "Advanced Git"
    - `git config`: Git is highly customizable
    - `git clone --depth=1`: shallow clone, without entire version history
    - `git add -p`: interactive staging
    - `git rebase -i`: interactive rebasing
    - `git blame`: show who last edited which line
    - `git stash`: temporarily remove modifications to working directory
    - `git bisect`: binary search history (e.g. for regressions)
    - `.gitignore`: specify intentionally untracked files to ignore