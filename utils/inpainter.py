import os, subprocess, time
from PIL import Image

class Inpainter:
    @staticmethod
    def content_aware_fill_using_ps(file_path: "img_path", save_path, photoshop_path=r"C:/Program Files/Adobe/Adobe Photoshop 2024/Photoshop.exe", extended_pixel = 15, checking_time = 0.1)->"np.ndarray":
        '''
        해당 메서드는 Windows 환경에서만 이용 가능합니다.
        '''
        #임시 파일 경로 생성
        file_path = os.path.abspath(file_path)
        print(file_path)
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

            var idautoCutout = stringIDToTypeID( "autoCutout" );
                var desc239 = new ActionDescriptor();
                var idsampleAllLayers = stringIDToTypeID( "sampleAllLayers" );
                desc239.putBoolean( idsampleAllLayers, false );
            executeAction( idautoCutout, desc239, DialogModes.NO );

            var idExpn = charIDToTypeID( "Expn" );
                var desc244 = new ActionDescriptor();
                var idBy = charIDToTypeID( "By  " );
                var idPxl = charIDToTypeID( "#Pxl" );
                desc244.putUnitDouble( idBy, idPxl, {extended_pixel} );
                var idselectionModifyEffectAtCanvasBounds = stringIDToTypeID( "selectionModifyEffectAtCanvasBounds" );
                desc244.putBoolean( idselectionModifyEffectAtCanvasBounds, false );
            executeAction( idExpn, desc244, DialogModes.NO );

            // =======================================================
            var idFl = charIDToTypeID( "Fl  " );
                var desc12 = new ActionDescriptor();
                var idUsng = charIDToTypeID( "Usng" );
                var idFlCn = charIDToTypeID( "FlCn" );
                var idcontentAware = stringIDToTypeID( "contentAware" );
                desc12.putEnumerated( idUsng, idFlCn, idcontentAware );
                var idOpct = charIDToTypeID( "Opct" );
                var idPrc = charIDToTypeID( "#Prc" );
                desc12.putUnitDouble( idOpct, idPrc, 100.000000 );
                var idMd = charIDToTypeID( "Md  " );
                var idBlnM = charIDToTypeID( "BlnM" );
                var idNrml = charIDToTypeID( "Nrml" );
                desc12.putEnumerated( idMd, idBlnM, idNrml );
            executeAction( idFl, desc12, DialogModes.NO );

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

        jsx_file_path = "inpainting.jsx"
        with open(jsx_file_path, "w") as file:
            file.write(jsx_code)
        # 스크립트 실행
        subprocess.Popen([photoshop_path, jsx_file_path])

        
        save_path = save_path.replace("\\\\", "/")
        
        
        # 스크립트 실행이 완료되어 배경 제거 파일이 생성될 때 까지 대기
        while not os.path.exists(save_path):
            time.sleep(checking_time)
        
    @staticmethod
    def content_aware_fill_square_using_ps(file_path: "img_path", save_path, top, bottom, left, right, extended_pixel = 15, checking_time = 0.1, photoshop_path=r"C:/Program Files/Adobe/Adobe Photoshop 2024/Photoshop.exe")->"np.ndarray":
        '''
        해당 메서드는 Windows 환경에서만 이용 가능합니다.
        '''
        #임시 파일 경로 생성
        file_path = os.path.abspath(file_path)
        print(file_path)
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
                var desc532 = new ActionDescriptor();
                var idnull = charIDToTypeID( "null" );
                    var ref23 = new ActionReference();
                    var idChnl = charIDToTypeID( "Chnl" );
                    var idfsel = charIDToTypeID( "fsel" );
                    ref23.putProperty( idChnl, idfsel );
                desc532.putReference( idnull, ref23 );
                var idT = charIDToTypeID( "T   " );
                    var desc533 = new ActionDescriptor();
                    var idTop = charIDToTypeID( "Top " );
                    var idPxl = charIDToTypeID( "#Pxl" );
                    desc533.putUnitDouble( idTop, idPxl, "{top}" );
                    var idLeft = charIDToTypeID( "Left" );
                    var idPxl = charIDToTypeID( "#Pxl" );
                    desc533.putUnitDouble( idLeft, idPxl, "{left}" );
                    var idBtom = charIDToTypeID( "Btom" );
                    var idPxl = charIDToTypeID( "#Pxl" );
                    desc533.putUnitDouble( idBtom, idPxl, "{bottom}" );
                    var idRght = charIDToTypeID( "Rght" );
                    var idPxl = charIDToTypeID( "#Pxl" );
                    desc533.putUnitDouble( idRght, idPxl, "{right}" );
                var idRctn = charIDToTypeID( "Rctn" );
                desc532.putObject( idT, idRctn, desc533 );
            executeAction( idsetd, desc532, DialogModes.NO );


            var idExpn = charIDToTypeID( "Expn" );
                var desc244 = new ActionDescriptor();
                var idBy = charIDToTypeID( "By  " );
                var idPxl = charIDToTypeID( "#Pxl" );
                desc244.putUnitDouble( idBy, idPxl, {extended_pixel} );
                var idselectionModifyEffectAtCanvasBounds = stringIDToTypeID( "selectionModifyEffectAtCanvasBounds" );
                desc244.putBoolean( idselectionModifyEffectAtCanvasBounds, false );
            executeAction( idExpn, desc244, DialogModes.NO );

            // 컨텐츠 어웨어 필 수행
            var idFl = charIDToTypeID( "Fl  " );
                var desc12 = new ActionDescriptor();
                var idUsng = charIDToTypeID( "Usng" );
                var idFlCn = charIDToTypeID( "FlCn" );
                var idcontentAware = stringIDToTypeID( "contentAware" );
                desc12.putEnumerated( idUsng, idFlCn, idcontentAware );
                var idOpct = charIDToTypeID( "Opct" );
                var idPrc = charIDToTypeID( "#Prc" );
                desc12.putUnitDouble( idOpct, idPrc, 100.000000 );
                var idMd = charIDToTypeID( "Md  " );
                var idBlnM = charIDToTypeID( "BlnM" );
                var idNrml = charIDToTypeID( "Nrml" );
                desc12.putEnumerated( idMd, idBlnM, idNrml );
            executeAction( idFl, desc12, DialogModes.NO );

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

        jsx_file_path = "inpainting.jsx"
        with open(jsx_file_path, "w") as file:
            file.write(jsx_code)
        # 스크립트 실행
        subprocess.Popen([photoshop_path, jsx_file_path])

        
        save_path = save_path.replace("\\\\", "/")
        
        
        # 스크립트 실행이 완료되어 배경 제거 파일이 생성될 때 까지 대기
        while not os.path.exists(save_path):
            time.sleep(checking_time)

    @staticmethod
    def content_aware_extend_using_ps(file_path: "img_path", save_path, checking_time = 0.1, photoshop_path=r"C:/Program Files/Adobe/Adobe Photoshop 2024/Photoshop.exe")->"np.ndarray":
        '''
        해당 메서드는 Windows 환경에서만 이용 가능합니다.
        '''
        #임시 파일 경로 생성
        file_path = os.path.abspath(file_path)
        print(file_path)
        image = Image.open(file_path)
        width, height = image.size
        #JSX 파일에 적합한 파일 경로로 replace
        open_path = file_path.replace("\\", "\\\\")
        save_path = save_path.replace("\\", "\\\\")
        #백그라운드 제거에 사용될 JSX파일
        prompt = r""""""""
        json_string = r'"""{"enable_mts":false}"""'
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

            var idCnvS = charIDToTypeID( "CnvS" );
                var desc430 = new ActionDescriptor();
                var idWdth = charIDToTypeID( "Wdth" );
                var idPxl = charIDToTypeID( "#Pxl" );
                desc430.putUnitDouble( idWdth, idPxl, "{str(height * 2)}");
                var idHrzn = charIDToTypeID( "Hrzn" );
                var idHrzL = charIDToTypeID( "HrzL" );
                var idCntr = charIDToTypeID( "Cntr" );
                desc430.putEnumerated( idHrzn, idHrzL, idCntr );
            executeAction( idCnvS, desc430, DialogModes.NO );

            var idsetd = charIDToTypeID( "setd" );
                var desc532 = new ActionDescriptor();
                var idnull = charIDToTypeID( "null" );
                    var ref23 = new ActionReference();
                    var idChnl = charIDToTypeID( "Chnl" );
                    var idfsel = charIDToTypeID( "fsel" );
                    ref23.putProperty( idChnl, idfsel );
                desc532.putReference( idnull, ref23 );
                var idT = charIDToTypeID( "T   " );
                    var desc533 = new ActionDescriptor();
                    var idTop = charIDToTypeID( "Top " );
                    var idPxl = charIDToTypeID( "#Pxl" );
                    desc533.putUnitDouble( idTop, idPxl, 0 );
                    var idLeft = charIDToTypeID( "Left" );
                    var idPxl = charIDToTypeID( "#Pxl" );
                    desc533.putUnitDouble( idLeft, idPxl, "{str((height * 2 - width)//2)}" );
                    var idBtom = charIDToTypeID( "Btom" );
                    var idPxl = charIDToTypeID( "#Pxl" );
                    desc533.putUnitDouble( idBtom, idPxl, "{height}" );
                    var idRght = charIDToTypeID( "Rght" );
                    var idPxl = charIDToTypeID( "#Pxl" );
                    desc533.putUnitDouble( idRght, idPxl, "{str((height * 2 + width)//2)}" );
                var idRctn = charIDToTypeID( "Rctn" );
                desc532.putObject( idT, idRctn, desc533 );
            executeAction( idsetd, desc532, DialogModes.NO );

            // 반전선택
            var idInvs = charIDToTypeID( "Invs" );
            executeAction( idInvs, undefined, DialogModes.NO );

            // 컨텐츠 어웨어 필 수행
            var idFl = charIDToTypeID( "Fl  " );
                var desc12 = new ActionDescriptor();
                var idUsng = charIDToTypeID( "Usng" );
                var idFlCn = charIDToTypeID( "FlCn" );
                var idcontentAware = stringIDToTypeID( "contentAware" );
                desc12.putEnumerated( idUsng, idFlCn, idcontentAware );
                var idOpct = charIDToTypeID( "Opct" );
                var idPrc = charIDToTypeID( "#Prc" );
                desc12.putUnitDouble( idOpct, idPrc, 100.000000 );
                var idMd = charIDToTypeID( "Md  " );
                var idBlnM = charIDToTypeID( "BlnM" );
                var idNrml = charIDToTypeID( "Nrml" );
                desc12.putEnumerated( idMd, idBlnM, idNrml );
            executeAction( idFl, desc12, DialogModes.NO );

            // 저장과 종료
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
        jsx_file_path = "inpainting.jsx"
        with open(jsx_file_path, "w") as file:
            file.write(jsx_code)
        # 스크립트 실행
        subprocess.Popen([photoshop_path, jsx_file_path])

        
        save_path = save_path.replace("\\\\", "/")
        
        
        # 스크립트 실행이 완료되어 배경 제거 파일이 생성될 때 까지 대기
        while not os.path.exists(save_path):
            time.sleep(checking_time)

    @staticmethod
    def generative_extend_using_ps(file_path: "img_path", save_path, checking_time = 0.1, photoshop_path=r"C:/Program Files/Adobe/Adobe Photoshop 2024/Photoshop.exe")->"np.ndarray":
        '''
        해당 메서드는 Windows 환경에서만 이용 가능합니다.
        '''
        #임시 파일 경로 생성
        file_path = os.path.abspath(file_path)
        print(file_path)
        image = Image.open(file_path)
        width, height = image.size
        #JSX 파일에 적합한 파일 경로로 replace
        open_path = file_path.replace("\\", "\\\\")
        save_path = save_path.replace("\\", "\\\\")
        #백그라운드 제거에 사용될 JSX파일
        prompt = r'""""""'
        json_string = r'"""{"enable_mts":true}"""'
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

            var idCnvS = charIDToTypeID( "CnvS" );
                var desc430 = new ActionDescriptor();
                var idWdth = charIDToTypeID( "Wdth" );
                var idPxl = charIDToTypeID( "#Pxl" );
                desc430.putUnitDouble( idWdth, idPxl, "{str(height * 2)}");
                var idHrzn = charIDToTypeID( "Hrzn" );
                var idHrzL = charIDToTypeID( "HrzL" );
                var idCntr = charIDToTypeID( "Cntr" );
                desc430.putEnumerated( idHrzn, idHrzL, idCntr );
            executeAction( idCnvS, desc430, DialogModes.NO );

            var idsetd = charIDToTypeID( "setd" );
                var desc532 = new ActionDescriptor();
                var idnull = charIDToTypeID( "null" );
                    var ref23 = new ActionReference();
                    var idChnl = charIDToTypeID( "Chnl" );
                    var idfsel = charIDToTypeID( "fsel" );
                    ref23.putProperty( idChnl, idfsel );
                desc532.putReference( idnull, ref23 );
                var idT = charIDToTypeID( "T   " );
                    var desc533 = new ActionDescriptor();
                    var idTop = charIDToTypeID( "Top " );
                    var idPxl = charIDToTypeID( "#Pxl" );
                    desc533.putUnitDouble( idTop, idPxl, 0 );
                    var idLeft = charIDToTypeID( "Left" );
                    var idPxl = charIDToTypeID( "#Pxl" );
                    desc533.putUnitDouble( idLeft, idPxl, "{str((height * 2 - width)//2)}" );
                    var idBtom = charIDToTypeID( "Btom" );
                    var idPxl = charIDToTypeID( "#Pxl" );
                    desc533.putUnitDouble( idBtom, idPxl, "{height}" );
                    var idRght = charIDToTypeID( "Rght" );
                    var idPxl = charIDToTypeID( "#Pxl" );
                    desc533.putUnitDouble( idRght, idPxl, "{str((height * 2 + width)//2)}" );
                var idRctn = charIDToTypeID( "Rctn" );
                desc532.putObject( idT, idRctn, desc533 );
            executeAction( idsetd, desc532, DialogModes.NO );

            // 반전선택
            var idInvs = charIDToTypeID( "Invs" );
            executeAction( idInvs, undefined, DialogModes.NO );

            // 컨텐츠 어웨어 필 수행

            var idsyntheticFill = stringIDToTypeID( "syntheticFill" );
                var desc566 = new ActionDescriptor();
                var idnull = charIDToTypeID( "null" );
                    var ref7 = new ActionReference();
                    var idDcmn = charIDToTypeID( "Dcmn" );
                    var idOrdn = charIDToTypeID( "Ordn" );
                    var idTrgt = charIDToTypeID( "Trgt" );
                    ref7.putEnumerated( idDcmn, idOrdn, idTrgt );
                desc566.putReference( idnull, ref7 );
                var idDocI = charIDToTypeID( "DocI" );
                desc566.putInteger( idDocI, 844 );
                var idLyrI = charIDToTypeID( "LyrI" );
                desc566.putInteger( idLyrI, 3 );
                var idprompt = stringIDToTypeID( "prompt" );
                desc566.putString( idprompt, {prompt} );
                var idserviceID = stringIDToTypeID( "serviceID" );
                desc566.putString( idserviceID, "clio" );
                var idMd = charIDToTypeID( "Md  " );
                var idsyntheticFillMode = stringIDToTypeID( "syntheticFillMode" );
                var idinpaint = stringIDToTypeID( "inpaint" );
                desc566.putEnumerated( idMd, idsyntheticFillMode, idinpaint );
                var idserviceOptionsList = stringIDToTypeID( "serviceOptionsList" );
                    var desc567 = new ActionDescriptor();
                    var idclio = stringIDToTypeID( "clio" );
                        var desc568 = new ActionDescriptor();
                        var idgi_PROMPT = stringIDToTypeID( "gi_PROMPT" );
                        desc568.putString( idgi_PROMPT, {prompt} );
                        var idgi_MODE = stringIDToTypeID( "gi_MODE" );
                        desc568.putString( idgi_MODE, "tinp" );
                        var idgi_SEED = stringIDToTypeID( "gi_SEED" );
                        desc568.putInteger( idgi_SEED, -1 );
                        var idgi_NUM_STEPS = stringIDToTypeID( "gi_NUM_STEPS" );
                        desc568.putInteger( idgi_NUM_STEPS, -1 );
                        var idgi_GUIDANCE = stringIDToTypeID( "gi_GUIDANCE" );
                        desc568.putInteger( idgi_GUIDANCE, 6 );
                        var idgi_SIMILARITY = stringIDToTypeID( "gi_SIMILARITY" );
                        desc568.putInteger( idgi_SIMILARITY, 0 );
                        var idgi_CROP = stringIDToTypeID( "gi_CROP" );
                        desc568.putBoolean( idgi_CROP, false );
                        var idgi_DILATE = stringIDToTypeID( "gi_DILATE" );
                        desc568.putBoolean( idgi_DILATE, false );
                        var idgi_CONTENT_PRESERVE = stringIDToTypeID( "gi_CONTENT_PRESERVE" );
                        desc568.putInteger( idgi_CONTENT_PRESERVE, 0 );
                        var idgi_ENABLE_PROMPT_FILTER = stringIDToTypeID( "gi_ENABLE_PROMPT_FILTER" );
                        desc568.putBoolean( idgi_ENABLE_PROMPT_FILTER, true );
                        var iddualCrop = stringIDToTypeID( "dualCrop" );
                        desc568.putBoolean( iddualCrop, true );
                        var idgi_ADVANCED = stringIDToTypeID( "gi_ADVANCED" );
                        desc568.putString( idgi_ADVANCED, {json_string} );
                    var idclio = stringIDToTypeID( "clio" );
                    desc567.putObject( idclio, idclio, desc568 );
                var idnull = charIDToTypeID( "null" );
                desc566.putObject( idserviceOptionsList, idnull, desc567 );
            executeAction( idsyntheticFill, desc566, DialogModes.NO );

            // 저장과 종료
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
            // 종료
            var idCls = charIDToTypeID( "Cls " );
                var desc683 = new ActionDescriptor();
                var idSvng = charIDToTypeID( "Svng" );
                var idYsN = charIDToTypeID( "YsN " );
                var idN = charIDToTypeID( "N   " );
                desc683.putEnumerated( idSvng, idYsN, idN );
                var idDocI = charIDToTypeID( "DocI" );
                desc683.putInteger( idDocI, 929 );
                var idforceNotify = stringIDToTypeID( "forceNotify" );
                desc683.putBoolean( idforceNotify, true );
            executeAction( idCls, desc683, DialogModes.NO );

        """
        jsx_file_path = "generative_fill.jsx"
        with open(jsx_file_path, "w") as file:
            file.write(jsx_code)
        # 스크립트 실행
        subprocess.Popen([photoshop_path, jsx_file_path])

        
        save_path = save_path.replace("\\\\", "/")
        
        
        # 스크립트 실행이 완료되어 배경 제거 파일이 생성될 때 까지 대기
        while not os.path.exists(save_path):
            time.sleep(checking_time)
