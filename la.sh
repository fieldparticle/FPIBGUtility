echo "/*! \page page2 Activity Log" > ../../DOCIN/actitivylog.dox
git log --since="Wed Feb 10" --pretty=format:'%h,%an,%ai,%s <br>' >> ../../DOCIN/actitivylog.dox
echo "*/<br>" >> ../../DOCIN/actitivylog.dox
