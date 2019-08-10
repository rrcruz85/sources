openerp.oemedical_odontology_exam_view_form = function (instance) {
	var _t = instance.web._t, _lt = instance.web._lt;
	var QWeb = instance.web.qweb;
	 
	var getPiecesRow1 = function () {
		return [{
			id: 'p18',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p17',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p16',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p15',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p14',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p13',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p12',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p11',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p21',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p22',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p23',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p24',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p25',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p26',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p27',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p28',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}];
	};

	var getPiecesRow2 = function () {
		return [{
			id: 'p55',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p54',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p53',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p52',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p51',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p61',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p62',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p63',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p64',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p65',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}];
	};

	var getPiecesRow3 = function () {
		return [{
			id: 'p85',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p84',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p83',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p82',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p81',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p71',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p72',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p73',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p74',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p75',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}];
	};

	var getPiecesRow4 = function () {
		return [{
			id: 'p48',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p47',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p46',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p45',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p44',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p43',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p42',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p41',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p31',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p32',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p33',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p34',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p35',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p36',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p37',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}, {
			id: 'p38',
			symbol: '',
			z1: '',
			z2: '',
			z3: '',
			z4: '',
			z5: ''
		}];
	};

	var piecesRow1 = getPiecesRow1();
	var piecesRow2 = getPiecesRow2();
	var piecesRow3 = getPiecesRow3();
	var piecesRow4 = getPiecesRow4();

	var selectedColor = 'red';

	var setDraggables = function () {
		let opacity = 0.85;
		$("#red-draggablePT").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			},          
		});
		$("#red-draggablePT").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#red-draggablePT").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		}); 

		$("#red-draggablePR").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			},     
		});
		$("#red-draggablePR").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#red-draggablePR").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		}); 

		$("#red-draggableO").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			},     
		});
		$("#red-draggableO").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#red-draggableO").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		});

		$("#red-draggableC").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			},     
		});
		$("#red-draggableC").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#red-draggableC").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		});

		$("#red-draggableF").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			},     
		});
		$("#red-draggableF").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#red-draggableF").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		});

		$("#red-draggableA").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			},    
		});
		$("#red-draggableA").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#red-draggableA").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		});

		$("#red-draggableK").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			},     
		});
		$("#red-draggableK").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#red-draggableK").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		});

		$("#red-draggableBSlash").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			},     
		});
		$("#red-draggableBSlash").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#red-draggableBSlash").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		});

		$("#red-draggableAster").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			},     
		});
		$("#red-draggableAster").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#red-draggableAster").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		});

		$("#red-draggableX").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			},     
		});
		$("#red-draggableX").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#red-draggableX").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		});

		$("#red-draggablePipe").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			},     
		});
		$("#red-draggablePipe").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#red-draggablePipe").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		});

		$("#red-draggableOO").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			},     
		});
		$("#red-draggableOO").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#red-draggableOO").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		});

		$("#red-draggableErase").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			},     
		});
		$("#red-draggableErase").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#red-draggableErase").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		});

		//-----Blue--------------------------
		$("#blue-draggablePT").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			}, 
		});
		$("#blue-draggablePT").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#blue-draggablePT").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		}); 

		$("#blue-draggablePR").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			}, 
		});
		$("#blue-draggablePR").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#blue-draggablePR").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		}); 

		$("#blue-draggableO").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			}, 
		});
		$("#blue-draggableO").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#blue-draggableO").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		}); 

		$("#blue-draggableC").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			}, 
		});
		$("#blue-draggableC").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#blue-draggableC").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		}); 

		$("#blue-draggableF").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			}, 
		});
		$("#blue-draggableF").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#blue-draggableF").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		}); 

		$("#blue-draggableA").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			}, 
		});
		$("#blue-draggableA").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#blue-draggableA").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		}); 

		$("#blue-draggableK").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			}, 
		});
		$("#blue-draggableK").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#blue-draggableK").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		}); 

		$("#blue-draggableBSlash").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			}, 
		});
		$("#blue-draggableBSlash").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#blue-draggableBSlash").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		}); 

		$("#blue-draggableAster").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			}, 
		});
		$("#blue-draggableAster").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#blue-draggableAster").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		}); 

		$("#blue-draggableX").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			}, 
		});
		$("#blue-draggableX").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#blue-draggableX").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		}); 

		$("#blue-draggablePipe").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			}, 
		});
		$("#blue-draggablePipe").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#blue-draggablePipe").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		}); 

		$("#blue-draggableOO").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			}, 
		});
		$("#blue-draggableOO").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#blue-draggableOO").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		}); 

		$("#blue-draggableErase").draggable({
			revert: "invalid",
			revertDuration: 100,
			opacity: opacity,
			drag: function( event, ui ) {
				$(this).removeClass('border-highlighted');         
			}, 
		});
		$("#blue-draggableErase").mouseenter(function(event) {
			$(this).addClass('border-highlighted');
		});  
		$("#blue-draggableErase").mouseleave(function(event) {
			$(this).removeClass('border-highlighted');
		}); 
	};

	var getPieceRow = function (id) {
		for (let i = 0; i < piecesRow1.length; i++) {
			if (piecesRow1[i].id == id) {
				return piecesRow1;
			}
		}

		for (let i = 0; i < piecesRow2.length; i++) {
			if (piecesRow2[i].id == id) {
				return piecesRow2;
			}
		}

		for (let i = 0; i < piecesRow3.length; i++) {
			if (piecesRow3[i].id == id) {
				return piecesRow3;
			}
		}

		for (let i = 0; i < piecesRow4.length; i++) {
			if (piecesRow4[i].id == id) {
				return piecesRow4;
			}
		}

		return [];
	};

	var getPiecePosition = function (id) {
		let pieceRow = getPieceRow(id);
		for (let i = 0; i < pieceRow.length; i++) {
			if (pieceRow[i].id == id) {
				return i;
			}
		}
	};

	var getPieceRowNumber = function (id) {
		for (let i = 0; i < piecesRow1.length; i++) {
			if (piecesRow1[i].id == id) {
				return 1;
			}
		}

		for (let i = 0; i < piecesRow2.length; i++) {
			if (piecesRow2[i].id == id) {
				return 2;
			}
		}

		for (let i = 0; i < piecesRow3.length; i++) {
			if (piecesRow3[i].id == id) {
				return 3;
			}
		}

		for (let i = 0; i < piecesRow4.length; i++) {
			if (piecesRow4[i].id == id) {
				return 4;
			}
		}

		return 0;
	};

	var getPiecesByRowId = function (id) {
		if (id == 1) {
			return piecesRow1;
		}
		else if (id == 2) {
			return piecesRow2;
		}
		else if (id == 3) {
			return piecesRow3;
		}
		else if (id == 4) {
			return piecesRow4;
		}
		else {
			return [];
		}
	};

	var setSpecialSymbol = function(id, symbol){
		let pieces = getPieceRow(id);
		for(let i=0; i < pieces.length; i++ ){
		   if(pieces[i].id == id){
			 pieces[i].symbol = symbol + '-' + (selectedColor == 'red' ? 'r' : 'b');
			 pieces[i].z1 = '';
			 pieces[i].z2 = '';
			 pieces[i].z3 = '';
			 pieces[i].z4 = '';
			 pieces[i].z5 = '';
			 break;
		   }  
		}
	};

	var clearPiece = function (id) {
		let pieces = getPieceRow(id);
		for (let i = 0; i < pieces.length; i++) {
			if (pieces[i].id == id) {
				pieces[i].symbol = '';
				pieces[i].z1 = '';
				pieces[i].z2 = '';
				pieces[i].z3 = '';
				pieces[i].z4 = '';
				pieces[i].z5 = '';
				break;
			}
		}
	};

	var setPiece = function (id, symbol, zoneId) {
		let pieces = getPieceRow(id);
		for (let i = 0; i < pieces.length; i++) {
			if (pieces[i].id == id) {
				pieces[i].symbol = '';
				switch (zoneId) {
					case '1': {
						pieces[i].z1 = symbol + '-' + (selectedColor == 'red' ? 'r' : 'b');
						break;
					}
					case '2': {
						pieces[i].z2 = symbol + '-' + (selectedColor == 'red' ? 'r' : 'b');
						break;
					}
					case '3': {
						pieces[i].z3 = symbol + '-' + (selectedColor == 'red' ? 'r' : 'b');
						break;
					}
					case '4': {
						pieces[i].z4 = symbol + '-' + (selectedColor == 'red' ? 'r' : 'b');
						break;
					}
					case '5': {
						pieces[i].z5 = symbol + '-' + (selectedColor == 'red' ? 'r' : 'b');
						break;
					}
				}
				break;
			}
		}
	};

	var hasSpecialSymbol = function (id) {
		let pieces = getPieceRow(id);
		for (let i = 0; i < pieces.length; i++) {
			if (pieces[i].id == id) {
				return pieces[i].symbol && pieces[i].symbol.length != 0;
			}
		}
	};

	var hasSymbol = function (id, symbol) {
		let pieces = getPieceRow(id);
		symbol += '-' + (selectedColor == 'red' ? 'r' : 'b');
		for (let i = 0; i < pieces.length; i++) {
			if (pieces[i].id == id) {
				return pieces[i].z1 == symbol || pieces[i].z2 == symbol || pieces[i].z3 == symbol || pieces[i].z4 == symbol || pieces[i].z5 == symbol;
			}
		}
	};

	var isEmpty = function(id){
		let pieces = getPieceRow(id);     
		for(let i=0; i < pieces.length; i++ ){
			 if(pieces[i].id == id){
				 return (!pieces[i].symbol && !pieces[i].z1 && !pieces[i].z2 && !pieces[i].z3 && !pieces[i].z4 && !pieces[i].z5);           
			 }  
		}
	};

	var getPiece = function (id) {
		let pieces = getPieceRow(id);
		for (let i = 0; i < pieces.length; i++) {
			if (pieces[i].id == id) {
				return pieces[i];
			}
		}
	};

	var toogleCross = function (id, zone, show) {
		var style = show ? 'inline' : 'none';
		let rowId = getPieceRowNumber(id);

		$('#' + id + '-x' + zone + '-1').css("display", style);
		$('#' + id + '-x' + zone + '-2').css("display", style);
		if (rowId == 2 || rowId == 3) {
			$('#' + id + '-x' + zone + '-c' + zone).css("display", style);
		}
	};

	var clearAll = function (id, show) {

		let rowId = getPieceRowNumber(id);
		if (rowId == 1 || rowId == 4) {
			$('#' + id + '-mainFrame').attr("stroke", "black");
			$('#' + id + '-mainFrame').attr("stroke-width", 3);

			$('#' + id + '-k1').css("display", "none");
			$('#' + id + '-k2').css("display", "none");
			$('#' + id + '-k3').css("display", "none");
			$('#' + id + '-k4').css("display", "none");
			$('#' + id + '-k5').css("display", "none");

			$('#' + id + '-t1').css("display", "none");
			$('#' + id + '-t2').css("display", "none");
			$('#' + id + '-t3').css("display", "none");
			$('#' + id + '-t4').css("display", "none");
			$('#' + id + '-t5').css("display", "none");

			$('#' + id + '-c1').css("display", "none");
			$('#' + id + '-c2').css("display", "none");
			$('#' + id + '-c3').css("display", "none");
			$('#' + id + '-c4').css("display", "none");
			$('#' + id + '-c5').css("display", "none");

		 	$('#' + id + '-pipe').css("display", "none");

			$('#' + id + '-ext1').css("display", "none");
			$('#' + id + '-ext2').css("display", "none");

			$('#' + id + '-pf1').css("display", "none");
			$('#' + id + '-pf2').css("display", "none");
		}
		else {
			$('#' + id + '-ool1').css("display", "none");
			$('#' + id + '-ool2').css("display", "none");
			$('#' + id + '-lext1').css("display", "none");
			$('#' + id + '-lext2').css("display", "none");
			$('#' + id + '-pipe').css("display", "none");

			$('#' + id + '-s1').css("display", "none");
			$('#' + id + '-s2').css("display", "none");
			$('#' + id + '-s3').css("display", "none");
			$('#' + id + '-s4').css("display", "none");
			$('#' + id + '-c4').css("display", "none");
			$('#' + id + '-x6-1').css("display", "none");
			$('#' + id + '-x6-2').css("display", "none");
			$('#' + id + '-t5-2').css("display", "none");

			$('#' + id + '-cc1').css("display", "none");
			$('#' + id + '-cc2').css("display", "none");
			$('#' + id + '-cc3').css("display", "none");
			$('#' + id + '-cc4').css("display", "none");
			$('#' + id + '-cc5').css("display", "none");

			$('#' + id + '-lext1').css("display", "none");
			$('#' + id + '-lext2').css("display", "none");

			$('#' + id + '-c1').attr("stroke-width", 2);
			$('#' + id + '-c1').attr("stroke", "black");
			$('#' + id + '-c1').attr("r", 29);

			$('#' + id + '-t1').css({
				'font-family': 'sans-serif',
				'font-weight': 'bold',
				'font-size': '16px',
				'display': 'none'
			});

			$('#' + id + '-t2').css({
				'font-family': 'sans-serif',
				'font-weight': 'bold',
				'font-size': '16px',
				'display': 'none'
			});

			$('#' + id + '-t3').css({
				'font-family': 'sans-serif',
				'font-weight': 'bold',
				'font-size': '16px',
				'display': 'none'
			});

			$('#' + id + '-t4').css({
				'font-family': 'sans-serif',
				'font-weight': 'bold',
				'font-size': '16px',
				'display': 'none'
			});

			$('#' + id + '-t5').css({
				'font-family': 'sans-serif',
				'font-weight': 'bold',
				'font-size': '16px',
				'display': 'none'
			});


			$('#' + id + '-t1').attr("x", 4);
			$('#' + id + '-t1').attr("y", 35);

			$('#' + id + '-t2').attr("x", 24);
			$('#' + id + '-t2').attr("y", 15);

			$('#' + id + '-t3').attr("x", 43);
			$('#' + id + '-t3').attr("y", 35);

			$('#' + id + '-t4').attr("x", 24);
			$('#' + id + '-t4').attr("y", 55);

			$('#' + id + '-t5').attr("x", 24);
			$('#' + id + '-t5').attr("y", 35);

		}

		$('#' + id + '-t1').html("");
		$('#' + id + '-t2').html("");
		$('#' + id + '-t3').html("");
		$('#' + id + '-t4').html("");
		$('#' + id + '-t5').html("");

		toogleCross(id, '1', show);
		toogleCross(id, '2', show);
		toogleCross(id, '3', show);
		toogleCross(id, '4', show);
		toogleCross(id, '5', show);

		clearPiece(id);
	};

	var showCorona = function (id, rowId, color = '') {

		clearAll(id, false);

		if (rowId == 1 || rowId == 4) {
			$('#' + id + '-t5').attr("fill", color || selectedColor);
			$('#' + id + '-t5').attr("x", 3);
			$('#' + id + '-t5').attr("y", 58);
			$('#' + id + '-t5').html('C');
			$('#' + id + '-t5').css({
				'font-size': '75px',
				'color': color || selectedColor,
				'display': 'inline'
			});
		}
		else {
			$('#' + id + '-t1').attr("fill", color || selectedColor);
			$('#' + id + '-t1').attr("x", 3);
			$('#' + id + '-t1').attr("y", 58);
			$('#' + id + '-t1').html('C');
			$('#' + id + '-t1').css({
				'font-family': 'sans-serif',
				'font-weight': 'bold',
				'font-size': '75px',
				'color': color || selectedColor,
				'display': 'inline'
			});
		}

		if(!color){
			$("#" + selectedColor + "-draggableC").css({
				left: 0,
				top: 0
			});
		}

		setSpecialSymbol(id, 'C');
	};

	var showExtraccion = function (id, rowId) {

		clearAll(id, false);

		if (rowId == 1 || rowId == 4) {
			$('#' + id + '-ext1').attr("stroke", selectedColor);
			$('#' + id + '-ext1').css('display', 'inline');

			$('#' + id + '-ext2').attr("stroke", selectedColor);
			$('#' + id + '-ext2').css('display', 'inline');
		}
		else {
			$('#' + id + '-lext1').attr("stroke", selectedColor);
			$('#' + id + '-lext1').css('display', 'inline');

			$('#' + id + '-lext2').attr("stroke", selectedColor);
			$('#' + id + '-lext2').css('display', 'inline');
		}

		$("#" + selectedColor + "-draggableX").css({
			left: 0,
			top: 0
		});

		setSpecialSymbol(id, 'X');
	};

	var showPipe = function (id) {

		clearAll(id, false);

		$('#' + id + '-pipe').attr("stroke", selectedColor);
		$('#' + id + '-pipe').css('display', 'inline');

		$("#" + selectedColor + "-draggablePipe").css({
			left: 0,
			top: 0
		});

		setSpecialSymbol(id, '|');
	};

	var showOO = function (id, rowId) {

		clearAll(id, false);

		if (rowId == 1 || rowId == 4) {
			$('#' + id + '-pf1').attr("stroke", selectedColor);
			$('#' + id + '-pf2').attr("stroke", selectedColor);

			$('#' + id + '-pf1').css('display', 'inline');
			$('#' + id + '-pf2').css('display', 'inline');
		}
		else {
			$('#' + id + '-ool1').attr("stroke", selectedColor);
			$('#' + id + '-ool2').attr("stroke", selectedColor);

			$('#' + id + '-ool1').css('display', 'inline');
			$('#' + id + '-ool2').css('display', 'inline');
		}

		$("#" + selectedColor + "-draggableOO").css({
			left: 0,
			top: 0
		});

		setSpecialSymbol(id, 'O-O');
	};

	var showProtesisTotal = function (id, rowId) {
		clearAll(id, false);

		if (rowId == 1 || rowId == 4) {
			$('#' + id + '-mainFrame').attr("stroke", selectedColor);
			$('#' + id + '-mainFrame').attr("stroke-width", 10);
		}
		else {
			$('#' + id + '-c1').attr("stroke", selectedColor);
			$('#' + id + '-c1').attr("stroke-width", 8);
			$('#' + id + '-c1').attr("r", 26);
		}

		$("#" + selectedColor + "-draggablePT").css({
			left: 0,
			top: 0
		});

		setSpecialSymbol(id, 'PT');
	};

	var showCarie = function(id, zone, rowId, color = '') {

		$('#' + id + '-t' + zone).css("display", "none");
		toogleCross(id, zone, false);

		if (rowId == 1 || rowId == 4) {
			$('#' + id + '-k' + zone).css("display", "none");
			$('#' + id + '-c' + zone).attr("fill", color || selectedColor);
			$('#' + id + '-c' + zone).css("display", "inline");
		}
		else {
			if (zone == '5') {
				$('#' + id + '-c4').attr("fill", "white");
				$('#' + id + '-c4').css("display", "inline");
				$('#' + id + '-x6-1').css("display", "none");
				$('#' + id + '-x6-2').css("display", "none");
				$('#' + id + '-t5-2').css("display", "none");
			}
			else {
				$('#' + id + '-s' + zone).css("display", "none");
			}

			$('#' + id + '-cc' + zone).attr("fill", color || selectedColor);
			$('#' + id + '-cc' + zone).css("display", "inline");
		}

		setPiece(id, 'O', zone);
	};

	var showCalza = function (id, zone, rowId, color = '') {

		toogleCross(id, zone, false);
		$('#' + id + '-t' + zone).css("display", "none");

		if (rowId == 1 || rowId == 4) {
			$('#' + id + '-c' + zone).css("display", "none");
			$('#' + id + '-k' + zone).attr("fill", color || selectedColor);
			$('#' + id + '-k' + zone).css("display", "inline");
		}
		else {
			$('#' + id + '-cc' + zone).css("display", "none");

			if (zone == '5') {
				$('#' + id + '-c4').attr("fill", color || selectedColor);
				$('#' + id + '-x6-1').css("display", "none");
				$('#' + id + '-x6-2').css("display", "none");
				$('#' + id + '-t5-2').css("display", "none");
			}
			else {
				let piece = getPiece(id);
				if (piece.z5 == '') {
					$('#' + id + '-x6-1').css("display", "inline");
					$('#' + id + '-x6-2').css("display", "inline");
					$('#' + id + '-c4').attr("fill", "white");
				}

				$('#' + id + '-s' + zone).attr("fill", color || selectedColor);
				$('#' + id + '-s' + zone).css("display", "inline");
			}
			$('#' + id + '-c4').css("display", "inline");
		}

		setPiece(id, 'K', zone);
	};

	var showSymbol = function (id, zone, symbol, rowId, color = '') {
		toogleCross(id, zone, false);

		if (rowId == 1 || rowId == 4) {
			$('#' + id + '-k' + zone).css("display", "none");
			$('#' + id + '-c' + zone).css("display", "none");

			$('#' + id + '-t' + zone).attr("fill", color || selectedColor);
			$('#' + id + '-t' + zone).css("color", color || selectedColor);
			$('#' + id + '-t' + zone).html(symbol);
			$('#' + id + '-t' + zone).css("display", "inline");
		}
		else {
			if (zone == '5') {

				if (hasSymbol(id, 'K')) {
					$('#' + id + '-c4').css("display", "inline");
					$('#' + id + '-x6-1').css("display", "none");
					$('#' + id + '-x6-2').css("display", "none");
					$('#' + id + '-t5-2').html(symbol);
					$('#' + id + '-t5-2').css({
						'font-family': 'sans-serif',
						'font-weight': 'bold',
						'font-size': '16px',
						"display": "inline"
					});
				}
				else {
					$('#' + id + '-c4').css("display", "none");
					$('#' + id + '-x6-1').css("display", "none");
					$('#' + id + '-x6-2').css("display", "none");
					$('#' + id + '-t5-2').css("display", "none");
				}
			}
			else {
				$('#' + id + '-s' + zone).css("display", "none");
			}

			$('#' + id + '-cc' + zone).css("display", "none");
			$('#' + id + '-t' + zone).attr("fill", color || selectedColor);
			$('#' + id + '-t' + zone).html(symbol);
			$('#' + id + '-t' + zone).css({
				'font-family': 'sans-serif',
				'font-weight': 'bold',
				"color": color || selectedColor,
				"display": "inline"
			});
		}

		setPiece(id, symbol, zone);
	};

	var getZoneNumber = function (id, event, rowId) {
		let imgPos = (rowId == 1 || rowId == 4) ? $('#' + id + '-main-square').position() : $('#' + id + '-main-circle').position();
		let width = (rowId == 1 || rowId == 4) ? $('#' + id + '-main-square').width() / 3 : $('#' + id + '-main-circle').width() / 3;
		let height = (rowId == 1 || rowId == 4) ? $('#' + id + '-main-square').height() / 3 : $('#' + id + '-main-circle').height() / 3;

		let pos_x = event.pageX;
		let pos_y = event.pageY;

		let x_pos = 1;
		let y_pos = 1;

		//X pos
		if (pos_x >= imgPos.left && pos_x < (imgPos.left + width)) {
			x_pos = 1;
		}
		else if (pos_x >= (imgPos.left + width) && pos_x < (imgPos.left + width * 2)) {
			x_pos = 2;
		}
		else if (pos_x >= (imgPos.left + width * 2) && pos_x <= (imgPos.left + width * 3)) {
			x_pos = 3;
		}

		//Y pos         
		if (pos_y >= imgPos.top && pos_y < (imgPos.top + height)) {
			y_pos = 1;
		}
		else if (pos_y >= (imgPos.top + height) && pos_y < (imgPos.top + height * 2)) {
			y_pos = 2;
		}
		else if (pos_y >= (imgPos.top + height * 2) && pos_y <= (imgPos.top + height * 3)) {
			y_pos = 3;
		}

		if (y_pos == 2 && x_pos == 1) {
			return '1';
		}
		else if (y_pos == 1) {
			return '2';
		}
		else if (y_pos == 2 && x_pos == 3) {
			return '3';
		}
		else if (y_pos == 3) {
			return '4'
		}
		else if (y_pos == 2 && x_pos == 2) {
			return '5';
		}
	};

	var areConsecutive = function (p1, p2) {
		let symbolWithColor = 'O-O-' + (selectedColor == 'red' ? 'r' : 'b');
		return p1.symbol == symbolWithColor && p2.symbol == symbolWithColor;
	};

	var isSpecialSymbol = function (symbol) {
		return symbol == 'PT' || symbol == 'C' || symbol == 'X' || symbol == '|' || symbol == 'O-O';
	};

	var consecutivePieceSequences = function (rowId) {

		let tmp_data = getPiecesByRowId(rowId);
		let consecutives = [];
		let length = tmp_data.length;
		if (length < 2) {
			return [];
		}
		else {

			let tmp_length = length;

			let cont = 1;
			while (tmp_length >= 2) {

				for (let i = 0; i < cont; i++) {

					let y = i;
					let end = length - cont + i;
					let allConsecutive = true;
					for (; y < end; y++) {
						if (!areConsecutive(tmp_data[y], tmp_data[y + 1])) {
							allConsecutive = false;
							break;
						}
					}
					if (allConsecutive) {

						let canSave = true;
						for (let z = 0; z < consecutives.length; z++) {
							if (consecutives[z].posi <= i && consecutives[z].posf >= i) {
								canSave = false;
								break;
							}
						}
						if (canSave) {
							consecutives.push({ posi: i, posf: end });
						}
					}
				}

				cont++;
				tmp_length--;
			}
			return consecutives;
		}
	};

	var hideLine = function(rowId){

		if (rowId == 1) {
			$('#p18-u').css('display', 'none');
			$('#p17-u').css('display', 'none');
			$('#p16-u').css('display', 'none');
			$('#p15-u').css('display', 'none');
			$('#p14-u').css('display', 'none');
			$('#p13-u').css('display', 'none');
			$('#p12-u').css('display', 'none');
			$('#p11-u').css('display', 'none');
			$('#p21-u').css('display', 'none');
			$('#p22-u').css('display', 'none');
			$('#p23-u').css('display', 'none');
			$('#p24-u').css('display', 'none');
			$('#p25-u').css('display', 'none');
			$('#p26-u').css('display', 'none');
			$('#p27-u').css('display', 'none');
			$('#p28-u').css('display', 'none');

			$('#p18-u').attr('stroke', selectedColor);
			$('#p17-u').attr('stroke', selectedColor);
			$('#p16-u').attr('stroke', selectedColor);
			$('#p15-u').attr('stroke', selectedColor);
			$('#p14-u').attr('stroke', selectedColor);
			$('#p13-u').attr('stroke', selectedColor);
			$('#p12-u').attr('stroke', selectedColor);
			$('#p11-u').attr('stroke', selectedColor);
			$('#p21-u').attr('stroke', selectedColor);
			$('#p22-u').attr('stroke', selectedColor);
			$('#p23-u').attr('stroke', selectedColor);
			$('#p24-u').attr('stroke', selectedColor);
			$('#p25-u').attr('stroke', selectedColor);
			$('#p26-u').attr('stroke', selectedColor);
			$('#p27-u').attr('stroke', selectedColor);
			$('#p28-u').attr('stroke', selectedColor);
		}
		else if (rowId == 2) {
			$('#p55-u').css('display', 'none');
			$('#p54-u').css('display', 'none');
			$('#p53-u').css('display', 'none');
			$('#p52-u').css('display', 'none');
			$('#p51-u').css('display', 'none');
			$('#p61-u').css('display', 'none');
			$('#p62-u').css('display', 'none');
			$('#p63-u').css('display', 'none');
			$('#p64-u').css('display', 'none');
			$('#p65-u').css('display', 'none');

			$('#p55-u').attr('stroke', selectedColor);
			$('#p54-u').attr('stroke', selectedColor);
			$('#p53-u').attr('stroke', selectedColor);
			$('#p52-u').attr('stroke', selectedColor);
			$('#p51-u').attr('stroke', selectedColor);
			$('#p61-u').attr('stroke', selectedColor);
			$('#p62-u').attr('stroke', selectedColor);
			$('#p63-u').attr('stroke', selectedColor);
			$('#p64-u').attr('stroke', selectedColor);
			$('#p65-u').attr('stroke', selectedColor);
		}
		else if (rowId == 3) {
			$('#p85-u').css('display', 'none');
			$('#p84-u').css('display', 'none');
			$('#p83-u').css('display', 'none');
			$('#p82-u').css('display', 'none');
			$('#p81-u').css('display', 'none');
			$('#p71-u').css('display', 'none');
			$('#p72-u').css('display', 'none');
			$('#p73-u').css('display', 'none');
			$('#p74-u').css('display', 'none');
			$('#p75-u').css('display', 'none');

			$('#p85-u').attr('stroke', selectedColor);
			$('#p84-u').attr('stroke', selectedColor);
			$('#p83-u').attr('stroke', selectedColor);
			$('#p82-u').attr('stroke', selectedColor);
			$('#p81-u').attr('stroke', selectedColor);
			$('#p71-u').attr('stroke', selectedColor);
			$('#p72-u').attr('stroke', selectedColor);
			$('#p73-u').attr('stroke', selectedColor);
			$('#p74-u').attr('stroke', selectedColor);
			$('#p75-u').attr('stroke', selectedColor);
		}
		else if (rowId == 4) {
			$('#p48-u').css('display', 'none');
			$('#p47-u').css('display', 'none');
			$('#p46-u').css('display', 'none');
			$('#p45-u').css('display', 'none');
			$('#p44-u').css('display', 'none');
			$('#p43-u').css('display', 'none');
			$('#p42-u').css('display', 'none');
			$('#p41-u').css('display', 'none');
			$('#p31-u').css('display', 'none');
			$('#p32-u').css('display', 'none');
			$('#p33-u').css('display', 'none');
			$('#p34-u').css('display', 'none');
			$('#p35-u').css('display', 'none');
			$('#p36-u').css('display', 'none');
			$('#p37-u').css('display', 'none');
			$('#p38-u').css('display', 'none');

			$('#p48-u').attr('stroke', selectedColor);
			$('#p47-u').attr('stroke', selectedColor);
			$('#p46-u').attr('stroke', selectedColor);
			$('#p45-u').attr('stroke', selectedColor);
			$('#p44-u').attr('stroke', selectedColor);
			$('#p43-u').attr('stroke', selectedColor);
			$('#p42-u').attr('stroke', selectedColor);
			$('#p41-u').attr('stroke', selectedColor);
			$('#p31-u').attr('stroke', selectedColor);
			$('#p32-u').attr('stroke', selectedColor);
			$('#p33-u').attr('stroke', selectedColor);
			$('#p34-u').attr('stroke', selectedColor);
			$('#p35-u').attr('stroke', selectedColor);
			$('#p36-u').attr('stroke', selectedColor);
			$('#p37-u').attr('stroke', selectedColor);
			$('#p38-u').attr('stroke', selectedColor);
		}

		$('#r' + rowId + 'sep1').css('display', 'none');
		$('#r' + rowId + 'sep2').css('display', 'none');
		$('#r' + rowId + 'sep3').css('display', 'none');
		$('#r' + rowId + 'sep4').css('display', 'none');
		$('#r' + rowId + 'sep5').css('display', 'none');
		$('#r' + rowId + 'sep6').css('display', 'none');
		$('#r' + rowId + 'sep7').css('display', 'none');
		$('#r' + rowId + 'sep8').css('display', 'none');

		if (rowId == 1 || rowId == 4) {
			$('#r' + rowId + 'sep9').css('display', 'none');
			$('#r' + rowId + 'sep10').css('display', 'none');
			$('#r' + rowId + 'sep11').css('display', 'none');
			$('#r' + rowId + 'sep12').css('display', 'none');
			$('#r' + rowId + 'sep13').css('display', 'none');
			$('#r' + rowId + 'sep14').css('display', 'none');
		}

		$('#r' + rowId + 'sep1').attr('stroke', selectedColor);
		$('#r' + rowId + 'sep2').attr('stroke', selectedColor);
		$('#r' + rowId + 'sep3').attr('stroke', selectedColor);
		$('#r' + rowId + 'sep4').attr('stroke', selectedColor);
		$('#r' + rowId + 'sep5').attr('stroke', selectedColor);
		$('#r' + rowId + 'sep6').attr('stroke', selectedColor);
		$('#r' + rowId + 'sep7').attr('stroke', selectedColor);
		$('#r' + rowId + 'sep8').attr('stroke', selectedColor);

		if (rowId == 1 || rowId == 4) {
			$('#r' + rowId + 'sep9').attr('stroke', selectedColor);
			$('#r' + rowId + 'sep10').attr('stroke', selectedColor);
			$('#r' + rowId + 'sep11').attr('stroke', selectedColor);
			$('#r' + rowId + 'sep12').attr('stroke', selectedColor);
			$('#r' + rowId + 'sep13').attr('stroke', selectedColor);
			$('#r' + rowId + 'sep14').attr('stroke', selectedColor);
		}

		$('#r' + rowId + 'lu1').css('display', 'none');
		$('#r' + rowId + 'lu2').css('display', 'none');
		$('#r' + rowId + 'lu3').css('display', 'none');
		$('#r' + rowId + 'lu4').css('display', 'none');
		$('#r' + rowId + 'luu').css('display', 'none');
		$('#r' + rowId + 'lu5').css('display', 'none');
		$('#r' + rowId + 'lu6').css('display', 'none');
		$('#r' + rowId + 'lu7').css('display', 'none');
		$('#r' + rowId + 'lu8').css('display', 'none');

		if (rowId == 1 || rowId == 4) {
			$('#r' + rowId + 'lu9').css('display', 'none');
			$('#r' + rowId + 'lu10').css('display', 'none');
			$('#r' + rowId + 'lu11').css('display', 'none');
			$('#r' + rowId + 'lu12').css('display', 'none');
			$('#r' + rowId + 'lu13').css('display', 'none');
			$('#r' + rowId + 'lu14').css('display', 'none');
		}

		$('#r' + rowId + 'lu1').attr('stroke', selectedColor);
		$('#r' + rowId + 'lu2').attr('stroke', selectedColor);
		$('#r' + rowId + 'lu3').attr('stroke', selectedColor);
		$('#r' + rowId + 'lu4').attr('stroke', selectedColor);
		$('#r' + rowId + 'luu').attr('stroke', selectedColor);
		$('#r' + rowId + 'lu5').attr('stroke', selectedColor);
		$('#r' + rowId + 'lu6').attr('stroke', selectedColor);
		$('#r' + rowId + 'lu7').attr('stroke', selectedColor);
		$('#r' + rowId + 'lu8').attr('stroke', selectedColor);

		if (rowId == 1 || rowId == 4) {
			$('#r' + rowId + 'lu9').attr('stroke', selectedColor);
			$('#r' + rowId + 'lu10').attr('stroke', selectedColor);
			$('#r' + rowId + 'lu11').attr('stroke', selectedColor);
			$('#r' + rowId + 'lu12').attr('stroke', selectedColor);
			$('#r' + rowId + 'lu13').attr('stroke', selectedColor);
			$('#r' + rowId + 'lu14').attr('stroke', selectedColor);
		}
	};

	var drawBridge = function (rowId) {

		hideLine(rowId);
		
		let consecutives = consecutivePieceSequences(rowId);
		let pieces = getPiecesByRowId(rowId);
  
		for (let i = 0; i < consecutives.length; i++) {
		  let p1 = pieces[consecutives[i].posi];
		  let p2 = pieces[consecutives[i].posf];
  
		  $('#' + p1.id + '-u').css('display', 'inline');
		  $('#' + p2.id + '-u').css('display', 'inline');
  
		  let limiti = 4;
		  let limitf = 5
		  if (rowId == 1 || rowId == 4) {
			limiti = 7;
			limitf = 8;
		  }
  
		  if (consecutives[i].posi <= limiti && consecutives[i].posf >= limitf) {
			$('#r' + rowId + 'luu').css('display', 'inline');
			for (let y = consecutives[i].posi; y < limiti; y++) {
			  $('#r' + rowId + 'lu' + (y + 1).toString()).css('display', 'inline');
			  $('#r' + rowId + 'sep' + (y + 1).toString()).css('display', 'inline');
			  $('#r' + rowId + 'sep' + (y + 1).toString()).children().attr('stroke', selectedColor);
			}
			for (let y = limitf; y < consecutives[i].posf; y++) {
			  $('#r' + rowId + 'lu' + y.toString()).css('display', 'inline');
			  $('#r' + rowId + 'sep' + y.toString()).css('display', 'inline');
			  $('#r' + rowId + 'sep' + y.toString()).children().attr('stroke', selectedColor);
			}
		  }
		  else {
  
			for (let y = consecutives[i].posi; y < consecutives[i].posf; y++) {
			  if (consecutives[i].posf <= limiti) {
				$('#r' + rowId + 'lu' + (y + 1).toString()).css('display', 'inline');
				$('#r' + rowId + 'sep' + (y + 1).toString()).css('display', 'inline');
				$('#r' + rowId + 'sep' + (y + 1).toString()).children().attr('stroke', selectedColor);
			  }
			  else {
				$('#r' + rowId + 'lu' + y.toString()).css('display', 'inline');
				$('#r' + rowId + 'sep' + y.toString()).css('display', 'inline');
				$('#r' + rowId + 'sep' + y.toString()).children().attr('stroke', selectedColor);
			  }
			}
		  }
		}		 
	};

	var drawUnion = function (rowId, id) {

		let piece = getPiece(id);
		let piecePos = getPiecePosition(id);
		let row = getPieceRow(id);
		let limit = rowId == 1 || rowId == 4 ? 7 : 4;

		for (let i = 0; i < row.length; i++) {
			if (row[i].symbol == 'PT-r' || row[i].symbol == 'PT-b') {

				if (i > 0 && (i - 1 != limit) && (row[i - 1].symbol == 'O-O-r' || row[i - 1].symbol == 'O-O-b')) {
					$('#r' + rowId + 'sep' + (i - 1 == 0 ? 1 : i > limit ? i - 1 : i).toString()).children().attr('stroke', selectedColor);
					$('#r' + rowId + 'sep' + (i - 1 == 0 ? 1 : i > limit ? i - 1 : i).toString()).css('display', 'inline');
				}

				if (i != limit && (i < row.length - 1) && (row[i + 1].symbol == 'O-O-r' || row[i + 1].symbol == 'O-O-b')) {
					$('#r' + rowId + 'sep' + (i > limit ? i : i + 1).toString()).children().attr('stroke', selectedColor);
					$('#r' + rowId + 'sep' + (i > limit ? i : i + 1).toString()).css('display', 'inline');
				}
			}
		}

		if (piece.symbol != 'O-O-r' && piece.symbol != 'O-O-b' && piece.symbol != 'PT-r' && piece.symbol != 'PT-b') {

			$('#r' + rowId + 'sep' + (piecePos > 0 ? piecePos : 1).toString()).css('display', 'none');

			if (piecePos < row.length) {
				$('#r' + rowId + 'sep' + piecePos.toString()).css('display', 'none');
			}
		}
	};

	var getSelectedSymbol = function(el){

		if(el.id == 'red-draggablePT' || el.id == 'blue-draggablePT'){
		   return 'PT';
		}
		else if(el.id == 'red-draggablePR' || el.id == 'blue-draggablePR'){
		 return 'W';
		}
		else if(el.id == 'red-draggableOO' || el.id == 'blue-draggableOO'){
		 return 'O-O';
		}
		else if(el.id == 'red-draggablePipe' || el.id == 'blue-draggablePipe'){
		 return '|';
		}
		else if(el.id == 'red-draggableC' || el.id == 'blue-draggableC'){
		 return 'C';
		}
		else if(el.id == 'red-draggableX' || el.id == 'blue-draggableX'){
		 return 'X';
		}
		else if(el.id == 'red-draggableA' || el.id == 'blue-draggableA'){
		 return 'A';
		}
		else if(el.id == 'red-draggableK' || el.id == 'blue-draggableK'){
		 return 'K';
		}
		else if(el.id == 'red-draggableO' || el.id == 'blue-draggableO'){
		 return 'O';
		}
		else if(el.id == 'red-draggableBSlash' || el.id == 'blue-draggableBSlash'){
		 return '/';
		}
		else if(el.id == 'red-draggableF' || el.id == 'blue-draggableF'){
		 return 'F';
		}
		else if(el.id == 'red-draggableAster' || el.id == 'blue-draggableAster'){
		 return '*';
		}	
		else if(el.id == 'red-delete' || el.id == 'blue-delete'){
			return 'DEL';
		} 	 
	};

	var resetPiece = function(id){
     
		let rowId = getPieceRowNumber(id);    
		let piecePos = getPiecePosition(id);      
		clearAll(id, true);

		$('#r' + rowId + 'sep' + (piecePos == 0 ? 1 : piecePos).toString()).css('display', 'none');
		$('#r' + rowId + 'sep' + (piecePos - 1 < 1 ? 1: piecePos - 1).toString()).css('display', 'none');  
			
		$("#" + selectedColor + "-delete").css({
			left: 0,
			top: 0
		});
	};
	
	var droppableFunction = function (id, event, ui, current_symbol = '', zone_Id = '') {

		let currentSymbol = !current_symbol ?  getSelectedSymbol(ui.helper[0]) : current_symbol;
		let rowId = getPieceRowNumber(id);
		
		if(currentSymbol == 'DEL'){
			resetPiece(id);
			drawBridge(rowId);
			drawUnion(rowId, id);
			return;
		}

		if(currentSymbol.endsWith('-r')){
			selectedColor = 'red';
			currentSymbol = currentSymbol.replace('-r', '');
		}

		if(currentSymbol.endsWith('-b')){
			selectedColor = 'blue';
			currentSymbol = currentSymbol.replace('-b', '');
		}		

		if (currentSymbol == 'PT') {
			showProtesisTotal(id, rowId);
		}
		else if (currentSymbol == 'C') {
			showCorona(id, rowId);
		}
		else if (currentSymbol == 'X') {
			showExtraccion(id, rowId);
		}
		else if (currentSymbol == '|') {
			showPipe(id);
		}
		else if (currentSymbol == 'O-O') {
			showOO(id, rowId);
		}

		if (isSpecialSymbol(currentSymbol)) {
			drawBridge(rowId);
			drawUnion(rowId, id);
			return;
		}

		if (hasSpecialSymbol(id)) {
			clearAll(id, true);
		}

		let zoneId = !zone_Id ? getZoneNumber(id, event, rowId) : zone_Id;

		if (currentSymbol == 'K') {
			showCalza(id, zoneId, rowId);
		}
		else if (currentSymbol == 'O') {
			showCarie(id, zoneId, rowId);
		}
		else {
			showSymbol(id, zoneId, currentSymbol, rowId);
		}

		drawBridge(rowId);
		drawUnion(rowId, id);

		if(!zone_Id){
			$("#" + ui.helper[0].id).css({
				left: 0,
				top: 0
			});
		}
	};

	var redrawSymbol = function(id, symbol, zoneId, rowId){

		var tmp = symbol.substring(0, 1);
		var color = symbol.endsWith('-r') ? 'red' : 'blue'; 

		if(tmp == 'K'){
			showCalza(id, zoneId, rowId, color);
		}
		else if(tmp == 'O'){
			showCarie(id, zoneId, rowId, color);
		}
		else{
			showSymbol(id, zoneId, tmp, rowId, color);
		}
	};

	var generateImg = function(id){
		var piece = jQuery.extend({}, getPiece(id)); 
		let rowId = getPieceRowNumber(id);        
		if(isEmpty(id)){       
			clearAll(id, false);
		} 
		else if(!hasSpecialSymbol(id)){ 
			clearAll(id, false);   

			if(!piece.z1) 
				toogleCross(id,'1', false);
			else
				redrawSymbol(id, piece.z1, '1', rowId);

			if(!piece.z2)
				toogleCross(id,'2', false);
			else
				redrawSymbol(id, piece.z2, '2', rowId);

			if(!piece.z3)
				toogleCross(id,'3', false);
			else         
				redrawSymbol(id, piece.z3, '3', rowId);

			if(!piece.z4)
				toogleCross(id,'4', false);
			else         
				redrawSymbol(id, piece.z4, '4', rowId);

			if(!piece.z5)
				toogleCross(id,'5', false);
			else         
				redrawSymbol(id, piece.z5, '5', rowId);        
		}        
		
		drawBridge(rowId);
		drawUnion(rowId, id);  
	};	

	var produceImg = function(){
	   
		for(let i = 0 ; i < piecesRow1.length; i++)
		{
		  generateImg(piecesRow1[i].id);
		}
		 
		for(let i = 0 ; i < piecesRow2.length; i++)
		{
		  generateImg(piecesRow2[i].id);
		}
		
		for(let i = 0 ; i < piecesRow3.length; i++)
		{
		  generateImg(piecesRow3[i].id);
		}
		
		for(let i = 0 ; i < piecesRow4.length; i++)
		{
		  generateImg(piecesRow4[i].id);
		}
  
		return html2canvas(document.getElementById('odontogram'));
	};

	instance.web.FormView.include({
		 
		load_form: function(data) {			
			var result = this._super(data);
		 	if(data.type == 'form'){
	
				if(data.model == 'oemedical.odontology.exam'){

				   	this.$el.find('.oe_form_container div.oe_form_sheet.oe_form_sheet_width').css("max-width", "1200px"); 
				
					if(this.$el.find('.oe_form_container').parent().hasClass('oe_form_readonly')){
						$('#row-symbols').addClass('hidden');
				   	}
					
					this.initOdontogram();

				}
				else{
			       this.$el.find('.oe_form_container div.oe_form_sheet.oe_form_sheet_width').css("max-width", "860px"); 
			    }
			}
			
			return result;
		},

		_actualize_mode: function(switch_to) {
			this._super(switch_to);
         	if(this.model == 'oemedical.odontology.exam'){
				
				if(this.$el.hasClass('oe_form_editable')){
					$('#row-symbols').removeClass('hidden');
				}
				else{
					$('#row-symbols').addClass('hidden');
					this.clearOdontogram();
					this.setPieces(this.datarecord, piecesRow1);
					this.setPieces(this.datarecord, piecesRow2);
					this.setPieces(this.datarecord, piecesRow3);
					this.setPieces(this.datarecord, piecesRow4);
				}
			}		
		},
		
		on_button_new: function() {
            this.clearOdontogram();            
			var result = this._super();
			return result;
		},
		
		_process_save: function(save_obj) {
			var self = this;
			var prepend_on_create = save_obj.prepend_on_create;
			try {
				var form_invalid = false,
					values = {},
					first_invalid_field = null,
					readonly_values = {};
				for (var f in self.fields) {
					if (!self.fields.hasOwnProperty(f)) { continue; }
					f = self.fields[f];
					if (!f.is_valid()) {
						form_invalid = true;
						if (!first_invalid_field) {
							first_invalid_field = f;
						}
					} else if (f.name !== 'id' && (!self.datarecord.id || f._dirty_flag)) {
						
						if (!f.get("readonly")) {
							values[f.name] = f.get_value();
						} else {
							readonly_values[f.name] = f.get_value();
						}
					}
				}
				 
				if (!self.datarecord.id && self.fields.sequence &&
					!_.has(values, 'sequence') && !_.isEmpty(self.dataset.cache)) {
					// Find current max or min sequence (editable top/bottom)
					var current = _[prepend_on_create ? "min" : "max"](
						_.map(self.dataset.cache, function(o){return o.values.sequence})
					);
					values['sequence'] = prepend_on_create ? current - 1 : current + 1;
				}
				if (form_invalid) {
					self.set({'display_invalid_fields': true});
					first_invalid_field.focus();
					self.on_invalid();
					return $.Deferred().reject();
				} else {
					self.set({'display_invalid_fields': false});
					var save_deferral;
				   
					//Modification
					if(self.dataset.model == 'oemedical.odontology.exam'){
						self.setDataPieces(values);	
					}                   

					if (!self.datarecord.id) {
						// Creation save
					    save_deferral = self.dataset.create(values, {readonly_fields: readonly_values}).then(function(r) {
							return self.record_created(r, prepend_on_create);
						}, null);
					} else if (_.isEmpty(values)) {
						// Not dirty, noop save
						save_deferral = $.Deferred().resolve({}).promise();
					} else {
						// Write save
						save_deferral = self.dataset.write(self.datarecord.id, values, {readonly_fields: readonly_values}).then(function(r) {
							return self.record_saved(r);
						}, null);
					     					    
					}
					return save_deferral;
				}
			} catch (e) {
				console.error(e);
				return $.Deferred().reject();
			}             
		},

		initOdontogram: function () {

			setDraggables();
			
			$("#red").prop("checked", true);
			$('#red-symbols').css('display', 'flex');
			$('#blue-symbols').css('display', 'none');			

			$("#red").click(function(){
				if($("#red").prop("checked")){         
				  selectedColor = 'red';
				  $('#red-symbols').css('display', 'flex');
				  $('#blue-symbols').css('display', 'none');
				}         
			});

			$("#blue").click(function(){
				if($("#blue").prop("checked")){         
				  selectedColor = 'blue';
				  $('#red-symbols').css('display', 'none');
				  $('#blue-symbols').css('display', 'flex');
				}  
			});

			$("#red-delete").draggable({  
				revert: "invalid",
				revertDuration: 100,    
				drag: function( event, ui ) {
					$(this).removeClass('border-highlighted');         
				}              
			});
			
			$("#red-delete").mouseenter(function(event) {
				$(this).addClass('border-highlighted');
			});
		
			$("#red-delete").mouseleave(function(event) {
				$(this).removeClass('border-highlighted');
			});
		
			$("#blue-delete").draggable({  
				revert: "invalid",
				revertDuration: 100,    
				drag: function( event, ui ) {
					$(this).removeClass('border-highlighted');         
				}              
			});
			
			$("#blue-delete").mouseenter(function(event) {
				$(this).addClass('border-highlighted');
			});
		
			$("#blue-delete").mouseleave(function(event) {
				$(this).removeClass('border-highlighted');
			});		

			var applyStyle = function (id) {
				var rowId = getPieceRowNumber(id);
	
				if (rowId == 1 || rowId == 4) {
					$('#' + id + '-mainFrame').attr('stroke-width', '8');
				}
				else {
					$('#' + id + '-c1').attr("stroke-width", '6');
					$('#' + id + '-c1').attr("r", '27');
				}
			};
	
			var removeStyle = function (id, ui) {
				var rowId = getPieceRowNumber(id);
				let currentSymbol = getSelectedSymbol(ui.helper[0]);
				
				if (currentSymbol != 'PT') {
	
					if (rowId == 1 || rowId == 4) {
						$('#' + id + '-mainFrame').attr('stroke-width', '3');
					}
					else {
						$('#' + id + '-c1').attr('stroke-width', '2');
						$('#' + id + '-c1').attr('r', '29');
					}
				}         
			};
	
			var removeStyleOut = function (id) {
				var rowId = getPieceRowNumber(id);      
				var piece = getPiece(id);
				
				if(piece.symbol == 'PT-r' || piece.symbol == 'PT-b')
				{
					if (rowId == 1 || rowId == 4) {
						$('#' + id + '-mainFrame').attr('stroke-width', '14');
					}
					else {
						$('#' + id + '-c1').attr("stroke-width", '8');
						$('#' + id + '-c1').attr("r", '26');
					}
					return;
				}
	
				if (rowId == 1 || rowId == 4) {
					$('#' + id + '-mainFrame').attr('stroke-width', '3');
				}
				else {
					$('#' + id + '-c1').attr('stroke-width', '2');
					$('#' + id + '-c1').attr('r', '29');
				}
			 
			};

			var setPiecesAsDroppable = function (pieceList) {
				for (let i = 0; i < pieceList.length; i++) {				 
					$("#" + pieceList[i].id).droppable({
						drop: function (event, ui) {           
							droppableFunction(pieceList[i].id, event, ui); 
							removeStyle(event.target.id, ui);
						},
						over: function (event, ui) {
							applyStyle(event.target.id);            
						},          
						out: function (event, ui) {
							removeStyleOut(event.target.id);                      
						}, 
					}); 
				} 
			}

			setPiecesAsDroppable(piecesRow1);
			setPiecesAsDroppable(piecesRow2);
			setPiecesAsDroppable(piecesRow3);
			setPiecesAsDroppable(piecesRow4);
		},		

		setPieces: function(datarecord, row){
			for(let i =0; i < row.length; i++){
				row[i].symbol = datarecord[row[i].id + '_symbol'];
				row[i].z1 = datarecord[row[i].id + '_z1'];
				row[i].z2 = datarecord[row[i].id + '_z2'];
				row[i].z3 = datarecord[row[i].id + '_z3'];
				row[i].z4 = datarecord[row[i].id + '_z4'];
				row[i].z5 = datarecord[row[i].id + '_z5'];

				if(row[i].symbol){
					droppableFunction(row[i].id, null, null, row[i].symbol, '1');
				}
				else{
					if(row[i].z1){
						droppableFunction(row[i].id, null, null, row[i].z1, '1');
					} 
					if(row[i].z2){
						droppableFunction(row[i].id, null, null, row[i].z2, '2');
					}
					if(row[i].z3){
						droppableFunction(row[i].id, null, null, row[i].z3, '3');
					}
					if(row[i].z4){
						droppableFunction(row[i].id, null, null, row[i].z4, '4');
					}
					if(row[i].z5){
						droppableFunction(row[i].id, null, null, row[i].z5, '5');
					}
				}
			}
		},
		
		setDataPieces: function(values){
			for(let i =0; i < piecesRow1.length; i++){
				values[piecesRow1[i].id + '_symbol'] = piecesRow1[i].symbol || false;
				values[piecesRow1[i].id + '_z1'] = piecesRow1[i].z1 || false;
				values[piecesRow1[i].id + '_z2'] = piecesRow1[i].z2 || false;
				values[piecesRow1[i].id + '_z3'] = piecesRow1[i].z3 || false;
				values[piecesRow1[i].id + '_z4'] = piecesRow1[i].z4 || false;
				values[piecesRow1[i].id + '_z5'] = piecesRow1[i].z5 || false;				
			}

			for(let i =0; i < piecesRow2.length; i++){
				values[piecesRow2[i].id + '_symbol'] = piecesRow2[i].symbol || false;
				values[piecesRow2[i].id + '_z1'] = piecesRow2[i].z1 || false;
				values[piecesRow2[i].id + '_z2'] = piecesRow2[i].z2 || false;
				values[piecesRow2[i].id + '_z3'] = piecesRow2[i].z3 || false;
				values[piecesRow2[i].id + '_z4'] = piecesRow2[i].z4 || false;
				values[piecesRow2[i].id + '_z5'] = piecesRow2[i].z5 || false;				
			}

			for(let i =0; i < piecesRow3.length; i++){
				values[piecesRow3[i].id + '_symbol'] = piecesRow3[i].symbol || false;
				values[piecesRow3[i].id + '_z1'] = piecesRow3[i].z1 || false;
				values[piecesRow3[i].id + '_z2'] = piecesRow3[i].z2 || false;
				values[piecesRow3[i].id + '_z3'] = piecesRow3[i].z3 || false;
				values[piecesRow3[i].id + '_z4'] = piecesRow3[i].z4 || false;
				values[piecesRow3[i].id + '_z5'] = piecesRow3[i].z5 || false;				
			}

			for(let i =0; i < piecesRow4.length; i++){
				values[piecesRow4[i].id + '_symbol'] = piecesRow4[i].symbol || false;
				values[piecesRow4[i].id + '_z1'] = piecesRow4[i].z1 || false;
				values[piecesRow4[i].id + '_z2'] = piecesRow4[i].z2 || false;
				values[piecesRow4[i].id + '_z3'] = piecesRow4[i].z3 || false;
				values[piecesRow4[i].id + '_z4'] = piecesRow4[i].z4 || false;
				values[piecesRow4[i].id + '_z5'] = piecesRow4[i].z5 || false;				
			}
		},
		
		clearOdontogram: function(){
			for(let i =0; i < piecesRow1.length; i++){
				clearAll(piecesRow1[i].id, true);				
			}
			for(let i =0; i < piecesRow2.length; i++){
				clearAll(piecesRow2[i].id, true);				
			}
			for(let i =0; i < piecesRow3.length; i++){
				clearAll(piecesRow3[i].id, true);				
			}
			for(let i =0; i < piecesRow4.length; i++){
				clearAll(piecesRow4[i].id, true);				
			}

			hideLine(1);
			hideLine(2);
			hideLine(3);
			hideLine(4);
		}
	});

	instance.web.Sidebar.include({

		on_item_action_clicked: function(item) {
			var self = this;
			self.getParent().sidebar_eval_context().done(function (sidebar_eval_context) {
				var ids = self.getParent().get_selected_ids();
				if (ids.length == 0) {
					instance.web.dialog($("<div />").text(_t("You must choose at least one record.")), { title: _t("Warning"), modal: true });
					return false;
				}
				var dataset = self.getParent().dataset;
				var active_ids_context = {
					active_id: ids[0],
					active_ids: ids,
					active_model: dataset.model
				}; 
				var c = instance.web.pyeval.eval('context',
					new instance.web.CompoundContext(
						sidebar_eval_context, active_ids_context));
				
				if(item.action.model == 'oemedical.odontology.exam' && item.action.name == 'Print Odontogram'){
					
					produceImg().then(function(canvas) {								
						//canvas.style.width = "525px";
						//canvas.style.height = "248px";
						//canvas.style.width = "50%";
						var generatedImg = canvas.toDataURL();
						
						var obj = {
							odontogram_img: generatedImg.substring(generatedImg.indexOf(",") + 1)
						};						

						dataset.write(ids[0], obj).then(function(r) {
                             
							self.rpc("/web/action/load", {
								action_id: item.action.id,
								context: new instance.web.CompoundContext(
									dataset.get_context(), active_ids_context).eval()
							}).done(function(result) {
								result.context = new instance.web.CompoundContext(result.context || {}, active_ids_context).set_eval_context(c);
								result.flags = result.flags || {};
								result.flags.new_window = true;
								self.do_action(result, {
									on_close: function() {
										// reload view
										self.getParent().reload();
									},
								});
							});							 

						}, null); 
					});					 
				}
				else{
                
					self.rpc("/web/action/load", {
						action_id: item.action.id,
						context: new instance.web.CompoundContext(
							dataset.get_context(), active_ids_context).eval()
					}).done(function(result) {
						result.context = new instance.web.CompoundContext(
							result.context || {}, active_ids_context)
								.set_eval_context(c);
						result.flags = result.flags || {};
						result.flags.new_window = true;
						self.do_action(result, {
							on_close: function() {
								// reload view
								self.getParent().reload();
							},
						});
					});
			    }
			});
		}
	});

	instance.web.form.WidgetButton.include({
		on_click: function() {
			var self = this;
			
			if(self.node.attrs.name == 'print_odontogram'){
                
				produceImg().then(function(canvas) {								
					 
					var generatedImg = canvas.toDataURL();
					
					var obj = {
						odontogram_img: generatedImg.substring(generatedImg.indexOf(",") + 1)
					};						
				 
					self.view.dataset.write(self.view.datarecord.id , obj).then(function(r) {
						
						self.force_disabled = true;
						self.check_disable();
						self.execute_action().always(function() {
							self.force_disabled = false;
							self.check_disable();
						});
					}, null);
					 
				});
			}
			else{
	
				this.force_disabled = true;
				this.check_disable();
				this.execute_action().always(function() {
					self.force_disabled = false;
					self.check_disable();
				});
			}
		},
	});
}