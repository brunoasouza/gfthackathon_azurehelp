import matplotlib.pyplot as plt
import seaborn as sns
from seaborn import matrix
from spacy.lang.fr.stop_words import STOP_WORDS


class CommonFunctions:
    def __init__(self):
        pass

    """ Plot the confusion matrix

        :param array cf_matrix: confusion matrix array
        :param bool  annot_value: If True, write the data value in each cell 
        :param str   cmap_value: matplotlib colormap name or object, or list of colors, optional
        :param str   fmt_value: String formatting code to use when adding annotations.
        :param str   title: Add title in the plot

    """
    def plot_confusion_matrix(self,
                              cf_matrix: list = [[23,  5],[ 3, 30]], 
                              annot_value: bool = True , 
                              cmap_value: str = 'Blues', 
                              fmt_value: str = '.1f',
                              fig_size: tuple = (11.7,8.27),
                              title: str = "Confusion matrix") -> None:

        print(cf_matrix)
        sns.set(rc={'figure.figsize':fig_size})
        ax = plt.axes()
        sns.heatmap(cf_matrix, annot=annot_value, cmap=cmap_value, fmt=fmt_value)
        ax.set_title(title)
        plt.show()

    """ Function to remove some special words from STOP_WORDS list

        :param str  word_to_check: word to check if exists on the list.
        :param list stop_words_list: Stop words list

        :return tupla: string with log and stopWords list
    """
    def nlp_function_remove_no_stop_words(self, word_to_check: str, stop_words_list: list = set(STOP_WORDS)):
        if word_to_check in stop_words_list:
            stop_words_list.remove(word_to_check)
            print(word_to_check + " was removed")
        else:
            print(word_to_check + " doesn't exist on dictionary")