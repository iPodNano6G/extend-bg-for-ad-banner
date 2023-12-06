from rembg import remove
import numpy as np
import cv2, os
import subprocess, time

class MaskGenerator:
    def make_mask_using_rembg(np_img):
        bg_removed_np_image = remove(np_img)
        #cv2.imwrite("bg_removed.png", bg_removed_np_image)
        mask_img = np.where(bg_removed_np_image[..., 3] >= 127, 0, 255).astype(np.uint8)
        return mask_img

    def make_mask_using_photoshop(np_img):
        pass

    def make_mask(np_img):
        mask_img = MaskGenerator.make_mask_using_rembg(np_img)
        return mask_img
    
    def load_mask(mask_folder, basename):
        files = os.listdir(mask_folder)
        for file_name in files:
            if basename in file_name:
                # 피사체는 검은색, 객체는 흰색 (h,w)
                bg_removed_np_image = cv2.imread(os.path.join(mask_folder, file_name), cv2.IMREAD_UNCHANGED)
                mask_img = np.where(bg_removed_np_image[..., 3] >= 63, 0, 255).astype(np.uint8)
                #cv2.imwrite("mask.png", mask_img)
                return mask_img
        raise RuntimeError("No such mask file")

    @staticmethod
    def remove_bg_using_ps(file_path: "img_path", save_path, photoshop_path=r"C:/Program Files/Adobe/Adobe Photoshop 2024/Photoshop.exe", checking_time = 0.1)->"np.ndarray":
        '''
        해당 메서드는 Windows 환경에서만 이용 가능합니다.
        '''
        #임시 파일 경로 생성
        file_path = os.path.abspath(file_path)
        #JSX 파일에 적합한 파일 경로로 replace
        open_path = file_path.replace("\\", "\\\\")
        save_path = save_path.replace("\\", "\\\\")
        #백그라운드 제거에 사용될 JSX파일
        jsx_code =  f"""
            var idOpn = charIDToTypeID( "Opn " );
                var desc288 = new ActionDescriptor();
                var iddontRecord = stringIDToTypeID( "dontRecord" );
                desc288.putBoolean( iddontRecord, false );
                var idforceNotify = stringIDToTypeID( "forceNotify" );
                desc288.putBoolean( idforceNotify, true );
                var idnull = charIDToTypeID( "null" );
                desc288.putPath( idnull, new File( "{open_path}" ) );
                var idDocI = charIDToTypeID( "DocI" );
                desc288.putInteger( idDocI, 77 );
                var idtemplate = stringIDToTypeID( "template" );
                desc288.putBoolean( idtemplate, false );
            executeAction( idOpn, desc288, DialogModes.NO );

            // ======================

            var idsetd = charIDToTypeID( "setd" );
                var desc303 = new ActionDescriptor();
                var idnull = charIDToTypeID( "null" );
                    var ref2 = new ActionReference();
                    var idLyr = charIDToTypeID( "Lyr " );
                    var idBckg = charIDToTypeID( "Bckg" );
                    ref2.putProperty( idLyr, idBckg );
                desc303.putReference( idnull, ref2 );
                var idT = charIDToTypeID( "T   " );
                    var desc304 = new ActionDescriptor();
                    var idOpct = charIDToTypeID( "Opct" );
                    var idPrc = charIDToTypeID( "#Prc" );
                    desc304.putUnitDouble( idOpct, idPrc, 100.000000 );
                    var idMd = charIDToTypeID( "Md  " );
                    var idBlnM = charIDToTypeID( "BlnM" );
                    var idNrml = charIDToTypeID( "Nrml" );
                    desc304.putEnumerated( idMd, idBlnM, idNrml );
                var idLyr = charIDToTypeID( "Lyr " );
                desc303.putObject( idT, idLyr, desc304 );
                var idLyrI = charIDToTypeID( "LyrI" );
                desc303.putInteger( idLyrI, 2 );
            executeAction( idsetd, desc303, DialogModes.NO );


            // ===================================================

            var idremoveBackground = stringIDToTypeID( "removeBackground" );
            executeAction( idremoveBackground, undefined, DialogModes.NO );


            // =======================================================
            var idsave = charIDToTypeID( "save" );
                var desc315 = new ActionDescriptor();
                var idAs = charIDToTypeID( "As  " );
                    var desc316 = new ActionDescriptor();
                    var idMthd = charIDToTypeID( "Mthd" );
                    var idPNGMethod = stringIDToTypeID( "PNGMethod" );
                    var idquick = stringIDToTypeID( "quick" );
                    desc316.putEnumerated( idMthd, idPNGMethod, idquick );
                    var idPGIT = charIDToTypeID( "PGIT" );
                    var idPGIT = charIDToTypeID( "PGIT" );
                    var idPGIN = charIDToTypeID( "PGIN" );
                    desc316.putEnumerated( idPGIT, idPGIT, idPGIN );
                    var idPNGf = charIDToTypeID( "PNGf" );
                    var idPNGf = charIDToTypeID( "PNGf" );
                    var idPGAd = charIDToTypeID( "PGAd" );
                    desc316.putEnumerated( idPNGf, idPNGf, idPGAd );
                    var idCmpr = charIDToTypeID( "Cmpr" );
                    desc316.putInteger( idCmpr, 6 );
                    var idembedIccProfileLastState = stringIDToTypeID( "embedIccProfileLastState" );
                    var idembedOff = stringIDToTypeID( "embedOff" );
                    var idembedOff = stringIDToTypeID( "embedOff" );
                    desc316.putEnumerated( idembedIccProfileLastState, idembedOff, idembedOff );
                var idPNGF = charIDToTypeID( "PNGF" );
                desc315.putObject( idAs, idPNGF, desc316 );
                var idIn = charIDToTypeID( "In  " );
                desc315.putPath( idIn, new File( "{save_path}" ) );
                var idDocI = charIDToTypeID( "DocI" );
                desc315.putInteger( idDocI, 81 );
                var idLwCs = charIDToTypeID( "LwCs" );
                desc315.putBoolean( idLwCs, true );
                var idEmbP = charIDToTypeID( "EmbP" );
                desc315.putBoolean( idEmbP, false );
                var idsaveStage = stringIDToTypeID( "saveStage" );
                var idsaveStageType = stringIDToTypeID( "saveStageType" );
                var idsaveBegin = stringIDToTypeID( "saveBegin" );
                desc315.putEnumerated( idsaveStage, idsaveStageType, idsaveBegin );
            executeAction( idsave, desc315, DialogModes.NO );

            // =======================================================
            var idCls = charIDToTypeID( "Cls " );
                var desc321 = new ActionDescriptor();
                var idDocI = charIDToTypeID( "DocI" );
                desc321.putInteger( idDocI, 81 );
                var idforceNotify = stringIDToTypeID( "forceNotify" );
                desc321.putBoolean( idforceNotify, true );
            executeAction( idCls, desc321, DialogModes.NO );    
        """
        jsx_file_path = "remove_background.jsx"
        with open(jsx_file_path, "w") as file:
            file.write(jsx_code)
        # 스크립트 실행
        subprocess.Popen([photoshop_path, jsx_file_path])

        save_path = save_path.replace("\\\\", "/")
        
        # 스크립트 실행이 완료되어 배경 제거 파일이 생성될 때 까지 대기
        while not os.path.exists(save_path):
            time.sleep(checking_time)
