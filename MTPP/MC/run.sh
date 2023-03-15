#!/bin/bash

markov() 
{
	train=Train_Cat
	test=Test_Cat
	for order in 1 2 3; do
	echo 'Order=' $order
	python markov_chain_baseline.py $1/$train $1/$test $order
	# python multiorder_markov_baseline.py $data_root/$train $data_root/$test $order
	done
}

# # For AI_JP
# echo "AI_JP"
# data_root=/home/vinayak/Desktop/My_Work/reuse/Codes/Clean_Data/AI_JP
# markov $data_root
# echo "========================================"

# # For CH_JP
# echo "CH_JP"
# data_root=/home/vinayak/Desktop/My_Work/reuse/Codes/Clean_Data/CH_JP
# markov $data_root
# echo "========================================"

# # For SA_JP
# echo "SA_JP"
# data_root=/home/vinayak/Desktop/My_Work/reuse/Codes/Clean_Data/SA_JP
# markov $data_root
# echo "========================================"

# # For MI_US
# echo "MI_US"
# data_root=/home/vinayak/Desktop/My_Work/reuse/Codes/Clean_Data/MI_US
# markov $data_root
# echo "========================================"

# # For NE_US
# echo "NE_US"
# data_root=/home/vinayak/Desktop/My_Work/reuse/Codes/Clean_Data/NE_US
# markov $data_root
# echo "========================================"

# # For VI_US
# echo "VI_US"
# data_root=/home/vinayak/Desktop/My_Work/reuse/Codes/Clean_Data/VI_US
# markov $data_root
# echo "========================================"

# For Appliances
echo "Appliances"
data_root=/home/vinayak/Desktop/My_Work/reuse/Codes/Amazon/Cleaned_Amazon/Appliances
markov $data_root
echo "========================================"

# For Beauty
echo "Beauty"
data_root=/home/vinayak/Desktop/My_Work/reuse/Codes/Amazon/Cleaned_Amazon/Beauty
markov $data_root
echo "========================================"

# For Fashion
echo "Fashion"
data_root=/home/vinayak/Desktop/My_Work/reuse/Codes/Amazon/Cleaned_Amazon/Fashion
markov $data_root
echo "========================================"