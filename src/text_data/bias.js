const bias =  {1: {
    header: "Our Biased Model",
    body: "Our biased model (biased in regards to race) was trained using a personally made dataset using the 2019 US Census data for reference. Thus, our biased dataset race distribution of the United States. The neural network configuations we used were the same."
},
2: {
    header: "Analysis",
    body: "As shown in the comparisons, a model trained on a biased dataset fails to pinpoint salient features of a face. For our current objective, this doesn't pose too large of a problem as the accuracy actually doesn't decrease by much. However, there are other situations where models trained on biased data can lead to discriminatory practices. For example, a facial recognition algorithm that does not detect salient features in a face could lead to misidentification that may aggravate issues in policing. Tangentially, there are similar problems in algorithms that power self-driving cars. Studies show that they are more likely to drive into black people. With a lack of representation in training data and in the technology field in general, these seemingly guileless discrepencies between accuracy of performance for different race groups can yield life-changing damage to communities if precipitously put into production."
}
};

export default {bias};