const modelInfo =  {1: {
    header: "Model",
    body: "Our model was trained using a convolutional neural network (CNN). We do not need to get into the details of how neural networks operate right now, but CNNs, which are used often for image processing, optimize what is known as filters. CNN filters have quite a lot in common with the filters in our everyday lives - they pick out the most important information and utilize them to make predictions. We will be unveiling the trained filters that showcase the salient features in a face, through XAI techniques."
},
2: {
    header: "XAI",
    body: "XAI, which is short for explainable AI, are methods used to explain the “black box” that is artificial learning. They help developers and the general public alike see the inner workings of a machine learning model. For our web application, we used explainable AI to visualize what a model would look like with and without bias. As you can see, our biased model did assign one of our three examples correctly. Without properly accessing the model with XAI techniques, we would’ve been unable to tell if our model was biased, and it could have posed difficulties in the future. There are three types of visualizations you can explore. Grad-CAM and guided back-propagation are similar and generated together. They both show the salient features in the last filter of our CNN. Red denotes the area with the most emphasis, while blue/purple represents the areas with less emphasis. The guided-backpropagation visualizations may make those areas more clear visually. On the other hand, integrated gradient visualizations are good for object localization. Given a particular category, the model will mark the areas in which they detect the object of your choosing. We’ve displayed the integrated gradients results with the category set as your predicted race, gender, and age."
}
};

export default {modelInfo};