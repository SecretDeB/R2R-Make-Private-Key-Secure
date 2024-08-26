import hashlib
import math

from bitarray import bitarray


class BloomFilter(object):
    def __init__(self, items_count, fp_prob, static_allocation=True, init_hash_count=1, bf_fixed_size=640,
                 hash_function="SHA256"):
        '''
        items_count : int
            Number of items expected to be stored in bloom filter
        fp_prob : float
            False Positive probability in decimal
        '''
        self.fp_prob = fp_prob

        self.hash_function=hash_function

        if static_allocation is True:
            self.size = bf_fixed_size
            self.hash_count = init_hash_count
        else:
            self.size = self.get_size(items_count, fp_prob)
            self.hash_count = self.get_hash_count(self.size, items_count)

        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)



    def get_bit_array(self):
        return self.bit_array

    def hash_compute(self, element):
        sha=hashlib.sha256()

        match self.hash_function:
            case "SHA1":
                sha = hashlib.sha1()
            case "SHA256":
                sha = hashlib.sha256()
            case "SHA512":
                sha = hashlib.sha512()
            case _:
                print("Enter valid hash function.")
        sha.update(element.encode('utf-8'))
        return sha.hexdigest()

    def add(self, item):
        '''
        Add an item in the filter
        '''
        digests = []
        # print(self.hash_count)
        for i in range(self.hash_count):
            # SHA Hash Function
            digest = int(self.hash_compute((item + str(i))), base=16) % self.size
            digests.append(digest)
            self.bit_array[digest] = True

    def display(self):
        '''
                Display the bloom filter bits
        '''
        for i in range(self.size):
            print(str(self.bit_array[i]) + " ", end="")
        print()

    def check(self, item):
        '''
        Check for existence of an item in filter
        '''
        for i in range(self.hash_count):
            digest = int(self.hash_compute((item + str(i))), base=16) % self.size
            if self.bit_array[digest] == False:
                return False
        return True

    @classmethod
    def get_size(self, n, p):
        '''
        Return the size of bit array(m) to used using the following formula
        m = -(n_items * lg(p)) / (lg(2)^2)
        n_items : int
            number of items to be stored in filter
        p : float
            False Positive probability in decimal
        '''
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        # print("M:",m)
        return int(m)

    @classmethod
    def get_hash_count(self, m, n):
        '''
        Return the hash function(k) to be used using the following formula
        k = (m/n_items) * lg(2)
        m : int
            size of bit array
        n_items : int
            number of items expected to be stored in filter
        '''
        k = (m / n) * math.log(2)
        # print("k:", k)
        return int(k)

    def get_load_factor(self):
        '''
        counts the number of one's comparing to bit array size
        '''
        count = self.bit_array.count(1)
        return count / self.size
