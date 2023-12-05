
            var idOpn = charIDToTypeID( "Opn " );
                var desc288 = new ActionDescriptor();
                var iddontRecord = stringIDToTypeID( "dontRecord" );
                desc288.putBoolean( iddontRecord, false );
                var idforceNotify = stringIDToTypeID( "forceNotify" );
                desc288.putBoolean( idforceNotify, true );
                var idnull = charIDToTypeID( "null" );
                desc288.putPath( idnull, new File( "C:\\projects\\extend-bg-for-ad-banner\\extract\\border_removed_result\\K720XX37458.jpg" ) );
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
                desc244.putUnitDouble( idBy, idPxl, 15 );
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
                desc315.putPath( idIn, new File( "C:\\projects\\extend-bg-for-ad-banner\\extract\\border_removed_result\\inpainting_1\\K720XX37458.png" ) );
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
        