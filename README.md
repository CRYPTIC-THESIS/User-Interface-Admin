# User-Interface-Admin
Admin User Interface
#
Checking the status and what branch you are currenly on
> git status

> git branch
#
Creating a New Branch (where you can edit and change the code)
> git checkout -b BranchName
#
Going to other branch
> git checkout BranchName
#
Commiting and Pushing changes to the Main Branch (After editing the code on your created branch)
*Note: This is done in your created branch*

> git add .

OR

> git add directory/of/the/file/changed.py


> git commit -m "Commit Description"

> git push origin BranchName

After Pushing, click the pull request link then Merge Pull Request if there are no errors or problems
#
*Note: Update the Main Branch Before Editing so that the code is up to date*
> git pull

#
Needed Packages/Libraries
> pip install tk

> pip install tkcalendar

> pip install Pillow

> pip install Pandas

> pip install firebase-admin

#
Update a Branch to the latest code from the Main Branch
>git checkout BranchName

>git merge main
