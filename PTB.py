class PTB :
    def __init__(self, fname) :
        import os
        fname, fextension = os.path.splitext(fname)
        self.fname = fname
        self.fextension = fextension

    def _pdf_to_jpg(self) :
        #return : opencv images list

        import numpy as np
        from pdf2image import convert_from_path

        poppler_path = r"C:\Users\ahnge\Anaconda3\envs\cv2\Library\bin"
        images = convert_from_path(self.fname+self.fextension, poppler_path=poppler_path)

        cv_images = []
        for i, img in enumerate(images) :
            #Save to jpg files
            #img.save(fname+'_'+str(i)+'.jpg')

            #Direct method : use PIL results
            np_img = np.array(img) #numpy array = opencv object
            cv_images.append(np_img)

        return cv_images 


    def _file_to_img(self) :
        #return : opencv img list / opencv img / None

        import cv2   

        if self.fextension == ".pdf" :
            result = self._pdf_to_jpg()
            return result 

        elif self.fextension == ".jpg" or ".jpeg" :
            img = cv2.imread(self.fname+self.fextension)
            return img

        else :
            return None


    def threshold(self) :
        #return : (now)None (maybe later)int

        import cv2

        src_list = self._file_to_img()
        for src in src_list :
            src = cv2.resize(src, None, fx=0.7, fy=0.7)
            b_img, g_img, r_img = cv2.split(src)

            def on_gray(val) :
                img_gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
                _, img_gray_binary = cv2.threshold(img_gray, val, 255, cv2.THRESH_BINARY_INV)
                img_gray_binary = cv2.bitwise_not(img_gray_binary)

                cv2.imshow('Gray_window', img_gray_binary)

            def on_R(val) :
                _, img_red_binary = cv2.threshold(r_img, val, 255, cv2.THRESH_BINARY_INV)
                img_red_binary = cv2.bitwise_not(img_red_binary)

                cv2.imshow('R_window', img_red_binary)

            def on_G(val) :
                _, img_green_binary = cv2.threshold(g_img, val, 255, cv2.THRESH_BINARY_INV)
                img_green_binary = cv2.bitwise_not(img_green_binary)

                cv2.imshow('G_window', img_green_binary)

            def on_B(val) :
                _, img_blue_binary = cv2.threshold(b_img, val, 255, cv2.THRESH_BINARY_INV)
                img_blue_binary = cv2.bitwise_not(img_blue_binary)

                cv2.imshow('G_window', img_blue_binary)

            cv2.namedWindow("Gray_window", cv2.WINDOW_NORMAL)
            cv2.namedWindow("R_window", cv2.WINDOW_NORMAL)
            cv2.namedWindow("G_window", cv2.WINDOW_NORMAL)
            cv2.namedWindow("B_window", cv2.WINDOW_NORMAL)

            cv2.imshow('Gray_window', src)
            cv2.imshow('R_window', src)
            cv2.imshow('G_window', src)
            cv2.imshow('B_window', src)

            cv2.createTrackbar('level', 'Gray_window', 0, 255, on_gray)
            cv2.createTrackbar('level', 'R_window', 0, 255, on_R)
            cv2.createTrackbar('level', 'G_window', 0, 255, on_G)
            cv2.createTrackbar('level', 'B_window', 0, 255, on_B)

            cv2.waitKey(0)
            # cv2.destroyAllWindows()


    def _hide_highlight(self, img) :
        #return : opencv img
        
        import cv2

        h, w, c = img.shape
        src = img
        b_img, g_img, r_img = cv2.split(img)

        #make threshold binary img
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        ret, img_multiple_binary = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY_INV)
        img_multiple_binary = cv2.bitwise_not(img_multiple_binary)

        img_gray = r_img
        ret, img_skyblue_binary = cv2.threshold(img_gray, 175, 255, cv2.THRESH_BINARY_INV)
        img_skyblue_binary = cv2.bitwise_not(img_skyblue_binary)
            
        #hide highlight compare with binary img
        for y in range(h) :  
            for x in range(w) :
                if img_multiple_binary[y, x] == 0 or img_skyblue_binary[y, x] == 0 : 
                    src.itemset(y, x, 0, 0)
                    src.itemset(y, x, 1, 0)
                    src.itemset(y, x, 2, 0)

        return src


    def block(self) :
        import cv2
        import os
        import numpy as np

        img_list = self._file_to_img()
        if np.all(img_list == None) :
            return
        
        elif type(img_list) != list : # an image
            src = self._hide_highlight(img_list)
            if not os.path.exists(self.fname) :
                os.makedirs(self.fname)
            cv2.imwrite(self.fname+'/'+self.fname+'.jpg', src)

        else :
            for i, img in enumerate(img_list) :
                src = self._hide_highlight(img)
                if not os.path.exists(self.fname) :
                    os.makedirs(self.fname)
                cv2.imwrite(self.fname+'/'+self.fname+'_'+str(i+1)+'.jpg', src)



#ver1. 굿노트 대표 색상 블락 : block
#ver2. 자기가 임계점 선택 : threshold, (later)block_ver2

ptb = PTB("0003.pdf")
# ptb.threshold()
# ptb.block()