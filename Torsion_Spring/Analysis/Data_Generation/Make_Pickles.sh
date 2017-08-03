for i in Analyze_Data_c.py Analyze_Data_d.py Analyze_Data_g.py Analyze_Data_i.py Analyze_Data_p.py Analyze_Data_s.py Analyze_Data_z.py
do
    for k in 0 1 2 3 4 5 6 7 8 9 
    do
        for j in 0.01
        do
            PRE="$j"
            POST="_np=3_$k"
            FILEN=$PRE$POST
            sed -i "s/SCRIPTNAME/$i/" Pickle_Data.sh
            sed -i "s/NUMBER/$FILEN/" Pickle_Data.sh
            qsub Pickle_Data.sh
            sed -i "s/$FILEN/NUMBER/" Pickle_Data.sh
            sed -i "s/$i/SCRIPTNAME/" Pickle_Data.sh
        done
    done
done
