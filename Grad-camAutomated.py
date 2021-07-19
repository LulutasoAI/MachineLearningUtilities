from keras import backend as K

class Grad_Cam_related():
    def __init__(self):
        pass

    def Grad_Cam(input_model, x, layer_name):
        X = np.expand_dims(x, axis=0)

        preprocessed_input = X/255.0

        input_model = model
        predictions = model.predict(preprocessed_input)
        class_idx = np.argmax(predictions[0])
        class_output = model.output[:, class_idx]

        conv_output = model.get_layer(layer_name).output
        grads = K.gradients(class_output, conv_output)[0]
        gradient_function = K.function([model.input], [conv_output, grads])

        output, grads_val = gradient_function([preprocessed_input])
        output, grads_val = output[0], grads_val[0]

        weights = np.mean(grads_val, axis=(0,1))
        cam = np.dot(output, weights)

        x = x.reshape(200,200,3)
        x = cv2.resize(x, (200, 200))
        cam = cv2.resize(cam, (200, 200), cv2.INTER_LINEAR)
        cam = np.maximum(cam,0)
        cam = cam/ cam.max()
        x
        jetcam = cv2.applyColorMap(np.uint8(255*cam), cv2.COLORMAP_JET)
        jetcam = cv2.cvtColor(jetcam, cv2.COLOR_BGR2RGB)
        jetcam = (np.float32(jetcam) + x /2)
        return jetcam

    def Grad_auto(self,model, x_test):
        for layer in model.layers:
            if "conv" in layer.name:
                target_layer = layer.name
        print(target_layer)
        for i, dt in enumerate(x_test):
            if i%10 == 0:
                cam = grad_cam(model, dt, target_layer)
                plt.subplot(1,2,1)
                plt.imshow(cam.astype(np.uint8))
                plt.subplot(1,2,2)
                plt.imshow(dt)
                plt.show()
