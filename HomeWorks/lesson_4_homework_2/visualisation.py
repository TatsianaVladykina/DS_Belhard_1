import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

class Visualizer:
    def __init__(self, dataset):
        self.dataset = dataset

    def Barplot(self, dataset, x, y):
        plt.bar(dataset[x], dataset[y], color='blue')
        plt.title('')
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()

    def Line(self, dataset, x, y):
        plt.plot(dataset[x], dataset[y], color='orange')
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(f'Зависит ли {y} от {x}?')
        plt.show()

    def Scatterplot(self, dataset, x, y):
        plt.scatter(dataset[x], dataset[y])
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()

    def Heatmap(self, dataset, annot=True, cmap='coolwarm'):
        plt.figure(figsize=(10, 8))
        sns.heatmap(dataset.corr(), annot=annot, cmap=cmap)
        plt.title('Correlation Heatmap')
        plt.show()

    def Pairplot(self, dataset, hue=None):
        sns.pairplot(dataset, hue=hue)
        plt.show()

    def Boxplot(self, dataset, x, y):
        sns.boxplot(x=dataset[x], y=dataset[y])
        plt.title(f'Boxplot of {y} by {x}')
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()

    def Histogram(self, dataset, column, bins=30, color='blue'):
        plt.hist(dataset[column], bins=bins, color=color)
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.show()


    def PieChart(self, dataset, column):
        plt.figure(figsize=(8, 8))
        plt.pie(dataset[column].value_counts(), labels=dataset[column].unique(), autopct='%1.1f%%', startangle=140)
        plt.title(f'Pie Chart of {column}')
        plt.show()

    def DonutChart(self, dataset, column):
        plt.figure(figsize=(8, 8))
        wedges, texts, autotexts = plt.pie(dataset[column].value_counts(), labels=dataset[column].unique(), autopct='%1.1f%%', startangle=140)
        for w in wedges:
            w.set_edgecolor('white')
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.title(f'Donut Chart of {column}')
        plt.show()
