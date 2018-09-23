import numpy as np
import matplotlib.pyplot as plt

class Model:
    def __init__(self):
        self.mean = 0
        self.var = 0.01

    def read_image(self,location):
        """This function reads image from path given by location"""

        """Load image"""
        self.orig_image = plt.imread(location)
        """remove alpha parameter if present"""
        if int(self.orig_image.shape[2])==4:
            self.orig_image = self.orig_image[0:,0:,0:3].copy()
        """Change all datatype to float64"""
        if issubclass(np.dtype(self.orig_image[0,0,0]).type, np.integer):
            self.orig_image = self.orig_image/255.0

        self.orig_image = self.orig_image.astype(np.float64);




    def show_orig_image(self):
        """This function show original image"""
        plt.imshow(self.orig_image)
        plt.show()



    def apply_noise(self):
        """This function apply gaussian noise and generate noisy image"""
        row,col,ch= self.orig_image.shape
        sigma = self.var**0.5
        gauss = np.random.normal(self.mean,sigma,(row,col,ch))
        gauss = gauss.reshape(row,col,ch)
        self.noisy = self.orig_image + gauss




    def show_noisy_image(self):
        """This function show noisy image"""
        plt.imshow(self.noisy)
        plt.show()



    def one_c_filter(self,source):
        """This function apply median filter on one channel of image"""
        members = np.zeros(9)
        members = members.astype(np.float64)

        final = np.zeros(source.shape)
        final = final.astype(np.float64)

        for y in range(1,source.shape[0]-1):
            for x in range(1,source.shape[1]-1):
                members[0] = source[y-1,x-1]
                members[1] = source[y,x-1]
                members[2] = source[y+1,x-1]
                members[3] = source[y-1,x]
                members[4] = source[y,x]
                members[5] = source[y+1,x]
                members[6] = source[y-1,x+1]
                members[7] = source[y,x+1]
                members[8] = source[y+1,x+1]
                members.sort()
                final[y,x]=members[4]
        return final



    def apply_filter(self):
        """This function calls above one channel filter to all three channel"""
        self.final_image = np.zeros(self.orig_image.shape)
        self.final_image[:,:,0] = self.one_c_filter(self.noisy[:,:,0])
        self.final_image[:,:,1] = self.one_c_filter(self.noisy[:,:,1])
        self.final_image[:,:,2] = self.one_c_filter(self.noisy[:,:,2])



    def show_final_image(self):
        """This function show final de-noised  image"""
        plt.imshow(self.final_image)
        plt.show()


    def save(self):
        """This function save all three images"""
        plt.imsave("./OUTPUT/original.jpg",self.orig_image)
        plt.imsave("./OUTPUT/noisy.jpg",np.clip(self.noisy,0,1))
        plt.imsave("./OUTPUT/filtered.jpg",np.clip(self.final_image,0,1))


def main():
    A = Model()
    s = input("Input name of file: ")
    A.read_image("./INPUT/" + s)
    A.show_orig_image()
    A.apply_noise()
    A.show_noisy_image()
    A.apply_filter()
    A.show_final_image()
    A.save()

if __name__ == "__main__":
    main()
