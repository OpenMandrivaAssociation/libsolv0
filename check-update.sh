#!/bin/sh
# Don't go past 0.6.x releases
git ls-remote --tags https://github.com/openSUSE/libsolv 2>/dev/null|awk '{ print $2; }' |grep -v '\^{}' |grep 'refs/tags/' |sed -e 's,refs/tags/,,;s,_,.,g' |grep '^0\.6\.' |sort -V |tail -n1
