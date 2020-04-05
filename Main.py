from PIL import Image, ImageDraw
import random

# name of the input image should be written on the next line inside the parentheses

image = Image.open("mountain.jpg")
width = image.width
height = image.height
pix = image.load()

image_size = 512
block_size = 10

# This function creates and returns a random generated image
def create_individual():
    ind_image = image.copy()
    ind = ImageDraw.Draw(ind_image)
    for i in range(image_size):
        for j in range(image_size):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            ind.point((i, j), (r, g, b))
    return ind_image

# This function takes as an argument the image, which fitness should be calculated and returns its fitness score
def fitness(img):
    fit_sum = 0
    fit_pix = img.load()
    for i in range(0, image_size - block_size, block_size):
        for j in range(0, image_size - block_size, block_size):
            for m in range(block_size):
                for n in range(block_size):
                    r = abs(pix[i + m, j + n][0] - fit_pix[i + n, j + n][0])
                    g = abs(pix[i + m, j + n][1] - fit_pix[i + n, j + n][1])
                    b = abs(pix[i + m, j + n][2] - fit_pix[i + n, j + n][2])
                    fit_sum = fit_sum + r + g + b
    return fit_sum

# Crossover takes 2 images(parents) as arguments and returns a child,
# which consists of best chosen squares of two parents on a coverage of 100 randomly taken squares
def crossover(img1, img2):
    child_img = img2.copy()
    pix1 = img1.load()
    pix2 = img2.load()
    child_pic = ImageDraw.Draw(child_img)
    for k in range(100):
        n = random.randint(0, image_size - block_size)
        m = random.randint(0, image_size - block_size)
        for i in range(block_size):
            for j in range(block_size):
                fit1 = 0
                fit2 = 0
                fit1 += abs(pix[n + i, m + j][0] - pix1[n + i, m + j][0])
                fit1 += abs(pix[n + i, m + j][1] - pix1[n + i, m + j][1])
                fit1 += abs(pix[n + i, m + j][2] - pix1[n + i, m + j][2])

                fit2 += abs(pix[n + i, m + j][0] - pix2[n + i, m + j][0])
                fit2 += abs(pix[n + i, m + j][1] - pix2[n + i, m + j][1])
                fit2 += abs(pix[n + i, m + j][2] - pix2[n + i, m + j][2])
                if fit1 < fit2:
                    child_pic.point((n + i, m + j), (pix1[n + i, m + j]))

    return child_img

# Mutation function takes an image as an arguments and returns another image,
# which is the mutated copy of the arguments picture
def mutation(img):
    mut_img = img.copy()
    mut_draw = ImageDraw.Draw(mut_img)
    pixel = img.load()
    for k in range(100):
        n = random.randint(0, image_size - block_size)
        m = random.randint(0, image_size - block_size)
        for i in range(block_size):
            for j in range(block_size):
                fit1 = 0
                fit2 = 0
                r = pixel[n + i, m + j][0] + random.randint(-255, 255)
                g = pixel[n + i, m + j][1] + random.randint(-255, 255)
                b = pixel[n + i, m + j][2] + random.randint(-255, 255)
                if r > 255:
                    r = 255
                if r < 0:
                    r = 0
                if g > 255:
                    g = 255
                if g < 0:
                    g = 0

                fit1 += abs(pix[n + i, m + j][0] - pixel[n + i, m + j][0])
                fit1 += abs(pix[n + i, m + j][1] - pixel[n + i, m + j][1])
                fit1 += abs(pix[n + i, m + j][2] - pixel[n + i, m + j][2])

                fit2 += abs(pix[n + i, m + j][0] - r)
                fit2 += abs(pix[n + i, m + j][1] - g)
                fit2 += abs(pix[n + i, m + j][2] - b)
                if fit1 > fit2:
                    mut_draw.point((n + i, m + j), (r, g, b))
    return mut_img

# best_fit function takes the population list as an arguments and
# returns two indexes of the individuals with the best fitness score from the population
def best_fit(pop_list):
    fit_pop = []
    index1 = 0
    index2 = 0
    for i in range(10):
        fit_pop.append(fitness(pop_list[i]))
    fit_pop1 = sorted(fit_pop)
    for i in range(10):
        if fit_pop1[0] == fit_pop[i]:
            index1 = i
        if fit_pop1[1] == fit_pop[i]:
            index2 = i
    return index1, index2

# worst_fit function works the same way as the best_fit,
# but returns the indexes of the two worst individuals
def worst_fit(pop_list):
    index1 = 0
    index2 = 0
    index3 = 0
    fit_pop = []
    for i in range(10):
        fit_pop.append(fitness(pop_list[i]))
    fit_pop1 = sorted(fit_pop)
    for i in range(10):
        if fit_pop1[9] == fit_pop[i]:
            index1 = i
        if fit_pop1[8] == fit_pop[i]:
            index2 = i
        if fit_pop1[7] == fit_pop[i]:
            index3 = i
    return index1, index2, index3


def main():
    population = []
    for i in range(10):
        population.append(create_individual())
    k = 0
    while True:
        best1_ind, best2_ind = best_fit(population)
        a = population[best1_ind]
        b = population[best2_ind]
        new_individ1 = crossover(a, b)
        new_individ2 = mutation(a)
        new_individ3 = mutation(b)
        index1, index2, index3 = worst_fit(population)
        population[index1] = new_individ1
        population[index2] = new_individ2
        population[index3] = new_individ3
        k += 1
        print("Generation " + str(k))
        print("Best: " + str(fitness(population[best1_ind])))

        if fitness(population[best1_ind]) < 40000000:
            population[best_fit(population)[0]].show()
            break
        if k % 50 == 0:
            population[best1_ind].show()


main()
