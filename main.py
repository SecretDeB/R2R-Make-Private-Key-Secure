import random
import time
import string
import re
import streamlit as st

from BLF import BloomFilter

padding = 0
bf = BloomFilter(0, 0)
key_size = 0
word_list = []
pk_length = 0

padding_flag = True


def prompt_security_questions():
    answers = []

    # print("Answrs are:", answers)
    # answers = ["Care", "Share", "Merry"]

    answers = [
        "The American singer-songwriter Taylor Swift has released 10 original studio albums, 4 re-recorded studio albums, 5 extended plays, and 4 live albums. She has sold an estimated 114 million album units worldwide and, in terms of pure sales, tallied 46.6 million in the United States and 7 million in the United Kingdom. According to the Recording Industry Association of America (RIAA), her albums have garnered 51 million certified units in the United States. As of February 2024, she is the solo artist with the most weeks (69) at number one on the US Billboard 200.",
        "Swift signed a recording contract with Big Machine Records in 2005 and released six albums with the label.",
        "Her tenth original studio album, Midnights (2022), was her fifth to sell over a million US first-week copies.",
        "All debuted at number one on the Billboard 200, and each of them sold over one million copies within the first release week in the United States.",
        "Her second, Fearless (2008), was the only album from the 2000s decade to spend one year in the top 10 of the Billboard 200"]
    return answers


def split_into_xor_values(key):
    numeric_representation = int(key, 2)

    # Choose another number of the same length in binary
    xor_part1 = random.randrange(pow(2, key_size) - 1)
    xor_part2 = numeric_representation ^ xor_part1

    return [format(xor_part1, f"0{key_size}b"),
            format(xor_part2, f"0{key_size}b")]


def add_padding(private_key):
    # return ("1" * padding) + private_key + ("1" * padding)
    return private_key + ("1" * padding)


# def insert_private_key(private_key, answers):
#     split_values = []
#     xor_part1, xor_part2 = split_into_xor_values(private_key)
#     split_values.append(xor_part1)
#     for i in range(1, len(answers) - 1):
#         xor_part1, xor_part2 = split_into_xor_values(xor_part2)
#         split_values.append(xor_part1)
#     split_values.append(xor_part2)
#
#     for i, answer in enumerate(answers):
#         for k in range(key_size):
#             answer += split_values[i][k]
#             # st.write(answer)
#             bf.add(answer)
#             # filter.display()
#     return bf.get_bit_array()

def insert_private_key(private_key, answers):
    answer_concat = ""
    for i in answers:
        answer_concat += i

    # print(private_key)
    temp_pk = list(private_key)  # temp private_key



    for i in temp_pk: 
        answer_concat += i
        # print(answer_concat)
        # st.write(answer_concat)
        bf.add(answer_concat)

    # end_time1 = time.time()
    # elapsed_time1 = (end_time1 - start_time1) * 1000
    # print(elapsed_time1)

    # for k in range(key_size):
    #     answer_concat += private_key[k]
    #     # st.write(answer_concat)
    #     bf.add(answer_concat)
    #     # filter.display()

    if not padding_flag:
        # print("here")
        # print(answer_concat)
        for word in word_list:
            # print(word)
            answer_concat += word
            # print(answer_concat)
            bf.add(answer_concat)

    return bf.get_bit_array()


def xor_two_lists(data1, data2):
    result = []
    for i in range(len(data1)):
        private_key = data1[i]
        for j in range(len(data2)):
            private_key ^= data2[j]
            result.append(private_key)
    return result


# def retrieve_private_key(answers):
#     split_values = [[] for _ in range(len(answers))]
#
#     for i, answer in enumerate(answers):
#         answer_len = len(answer)
#
#         random_value = random.choice([0, 1])
#         # print("randomValue1:", random_value)
#         # print("randomValue2:", 1 - random_value)
#
#         queue = [answer + str(random_value), answer + str(1 - random_value)]
#
#         while queue:
#             entry = queue.pop(0)
#             if bf.check(entry):
#                 # st.write(entry," Present")
#                 if len(entry) < answer_len + key_size:
#                     random_value = random.choice([0, 1])
#                     # print("randomValue1:", random_value)
#                     # print("randomValue2:", 1 - random_value)
#                     queue.append(entry + str(random_value))
#                     queue.append(entry + str(1 - random_value))
#                 else:
#                     # print("string:", entry[answer_len:])
#                     # print("num:", int(entry[answer_len:], 2))
#                     split_values[i].append(int(entry[answer_len:], 2))
#             # else:
#             #     st.write(entry, "Not Present")
#
#     # XOR all security questions answers
#     data1 = split_values[0]
#     data2 = split_values[1]
#     data1 = xor_two_lists(data1, data2)
#     for i in range(2, len(answers)):
#         data2 = split_values[i]
#         data1 = xor_two_lists(data1, data2)
#
#     return data1

def retrieve_private_key(answers):
    global pk_length

    split_values = []

    answer_concat = ""
    for i in answers:
        answer_concat += i
    answer_len = len(answer_concat)

    random_value = random.choice([0, 1])
    # print("randomValue1:", random_value)
    # print("randomValue2:", 1 - random_value)

    queue = [answer_concat + str(random_value), answer_concat + str(1 - random_value)]

    while queue:
        entry = queue.pop(0)
        if bf.check(entry):
            # print(entry," Present")
            if len(entry) < answer_len + pk_length:
                random_value = random.choice([0, 1])
                queue.append(entry + str(random_value))
                queue.append(entry + str(1 - random_value))
            else:
                split_values.append(int(entry[answer_len:], 2))
        # else:
        #     print(entry, "Not Present")

    return split_values


def initialize(hash_count, size, hash_function, sq_count, answers):
    global bf, word_list

    # hash_count=3
    # size=3680
    # if hash_count == 0 or size == 0:
    #     items_count = key_size * sq_count
    #     fp_prob = 0.00000000000000000000000000000000000000000000000000000000000000001
    #     static_allocation = False
    #     bf = BloomFilter(items_count, fp_prob, static_allocation, hash_function)
    #
    # else:
    #     static_allocation = True
    #     init_hash_count = hash_count
    #     bf_fixed_size = size
    #     bf = BloomFilter(0, 0, static_allocation, init_hash_count, bf_fixed_size, hash_function)

    # without padding
    if not padding_flag:
        word_list = []
        for i in answers:
            l = re.sub('[' + string.punctuation + ']', '', i).split()
            word_list.extend(l)
        print(word_list)
        print("Number of words:", str(len(word_list)))
        items_count = key_size + len(word_list)
    else:
        items_count = key_size

    print("Number of items (n):", str(items_count))

    fp_prob = 0.00000000000000000000000000000000000000000000000000000000000000001
    static_allocation = False
    bf = BloomFilter(items_count, fp_prob, static_allocation, hash_function)

    # st.write(bf.size)
    # st.write(bf.hash_count)


def insert(private_key, answers, hash_count=0, size=0, hash_function="SHA256"):
    # answers = prompt_security_questions()
    # private_key = "1000"
    # print("p:", private_key)
    global  pk_length

    # private_key = "1101101111000110110010101101101000111111000100101010100110111101101111010110101101011010101001111111110011011111100110100111110111111011001101000111100101111011100001100111101100101111000111110000100111111110011100110000110001110101000100100010101100101101"
    # for i in answers:
    #     st.write(i)
    #
    # st.write(private_key)
    # st.write(hash_count)
    # st.write(size)
    # st.write(hash_function)

    start_time = time.time()
    pk_length = len(private_key)

    print("Storing private key to bloom filter...")

    global key_size

    # with padding
    if padding_flag:
        private_key = add_padding(private_key)

    key_size = len(private_key)
    initialize(hash_count, size, hash_function, len(answers), answers)
    bit_array = insert_private_key(private_key, answers)

    # result = "Bloom filter: \n" + bit_array.to01() + "\n" + "Size of Bloom filter:" + \
    #          str(bf.size) + "\n" + "Number of hash function:" + str(bf.hash_count)

    result = "Size of Bloom filter:" + \
             str(bf.size) + "(" + str(
        float("{:.3f}".format(bf.size / (8 * (2 ** 10))))) + "KB)\n" + "Number of hash function:" + str(
        bf.hash_count) + "\n Bloom filter: \n" + bit_array.to01() + "\n"

    st.session_state.bit_array = result

    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000
    st.session_state.insertion_time = elapsed_time


def remove_padding(private_keys):
    result = []
    temp = "".join(["1" for _ in range(padding)])
    # print(temp)
    for i in private_keys:
        str_ = format(i, f"0{key_size}b")
        # print(str_)
        # result.append(str_[padding:len(str_) - padding])
        # print(len(str_)-padding)
        # print(len(str_))
        if str_[len(str_) - padding:len(str_)] == temp:
            result.append(str_[0:len(str_) - padding])
        # st.write(str_)
    return result


def remove_candidates_padding(private_keys, answers):
    global  pk_length
    key_set = set(private_keys)

    answer_concat = ""
    for i in answers:
        answer_concat += i

    # print(answer_concat)
    for j in range(1,padding+1):
        if len(key_set) != 1:
            for i in private_keys:
                entry = answer_concat + str(format(i, f"0{pk_length}b")) + "".join(["1" for _ in range(j)])
                # print(entry)
                if not bf.check(entry):
                    # print("here")
                    key_set.remove(i)
        else:
            break

    # print(key_set)
    return list(key_set)[0]


def remove_candidates(private_keys, answers):
    global word_list
    key_set = set(private_keys)

    answer_concat = ""
    for i in answers:
        answer_concat += i

    w = ""

    for word in word_list:
        # print(word)
        if len(key_set) != 1:
            w += word
            # print(w)
            for i in private_keys:
                entry = answer_concat + str(format(i, f"0{key_size}b")) + w
                # print(entry)
                # print(i)
                if not bf.check(entry):
                    key_set.remove(i)
                    # print("hree")
        else:
            break

    # print(key_set)
    return list(key_set)[0]


def retrieve(answers):
    # answers = prompt_security_questions()
    # for i in answers:
    #     st.write(i)

    start_time = time.time()

    print("Retrieving private key from bloom filter...")
    private_keys = retrieve_private_key(answers)
    # print(private_keys)
    print("number of candidate PK:", str(len(private_keys)))

    # private_keys=[i for i in range(15)]
    # print(len(private_keys))
    private_key = private_keys[0]
    # print(private_key)

    if padding_flag:
        if len(private_keys) > 1:
            private_key = remove_candidates_padding(private_keys, answers)
        # st.session_state.bit_array = "Private Key:\n"+str(format(private_key, f"0{key_size}b"))
    else:
        if len(private_keys) > 1:
            private_key = remove_candidates(private_keys, answers)
        # st.session_state.bit_array = "Private Key:\n"+str(format(private_key, f"0{key_size}b"))

    st.session_state.bit_array = "Private Key:\n" + str(format(private_key, f"0{pk_length}b"))

    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000
    st.session_state.retrieval_time = elapsed_time
