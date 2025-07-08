# 主目录
repo="$HOME/workspace/my/studies"
cd "$repo" || exit

commit_info="Init (Clear history commits)"

rm -rf .git
git init -b master
git config --local user.name imhuay
git config --local user.email imhuay@163.com
echo

printf "=== Start Push Main Repo ===\n"
git remote add origin "https://github.com/imhuay/studies.git"
git add -A
git commit -m "$commit_info"
git push --force --set-upstream origin master
echo

#printf "=== Start Push Src Repo ===\n"
#prefix="src"
#sub_name="sync_src"
#git remote add $sub_name "https://github.com/imhuay/$sub_name.git"
#sub_commit_id=$(git subtree split --prefix=$prefix --branch $sub_name --rejoin --squash)
#git push --force $sub_name "$sub_commit_id:master"
#echo
