
# Science and Engineering Journal Abbreviations 
#	http://woodward.library.ubc.ca/research-help/journal-abbreviations/

bakclist = [
'Z. Physik',
'Materials Science and Engineering: B',
]

#       Full name										Abbreviation							alias						mangled forms							
journals = [
(	'ACS Nano'											,	'ACS Nano'							,'ACSNano'		,[]	),
(   'Advances In Physics'                               ,   'Adv. Phys.'                        ,'AdvPhys'      ,[] ),
(	'Advanced Materials'								,	'Adv. Mater.'						,'AdvMat'		,[]	),
(	'Advanced Materials Interfaces'						,	'Adv. Mater. Interfaces'			,'AdvMatInt'	,[]	),
(	'Annals of the New York Academy of Sciences'		,	'Ann. N.Y. Acad. Sci.'				,'ANYASt'		,[]	),
(	'Applied Physics Letters'							,	'Appl. Phys. Lett.'					,'APL'			,[]	),
(	'Chemical Communications'							,	'Chem. Commun.'						,'ChemCom'		,[]	),
(	'Chemical Reviews'									,	'Chem. Rev.'						,'ChemRev'		,[]	),
(	'Chemical Society Reviews'							,	'Chem. Soc. Rev.'					,'ChemSocRev'	,[]	),
(	'Computational Materials Science'					,	'Comput. Mater. Sci.' 				,'CompMatSci'	,[ 'Comp. Mat. Sci.'	]	),
(	'Coordination Chemistry Reviews'					,	'Coord. Chem. Rev.'					,'CoordChemRev'	,[]	),
(	'Electrochimica Acta'								,	'Electrochim. Acta'					,'ElecActa'		,[]	),
(	'Europhysics Letters' 								,	'Europhys. Lett.'					,'EPL'			,[ 'EPL' ]	),
(	'Fluid Phase Equilibria'							,	'Fluid Phase Equilib.'				,'FluidPhEq'	,[]	),
(	'IBM Journal of Research and Development'			,	'IBM J. Res. Dev.'					,'IBMjrd'		,[]	),
(	'International Journal of Molecular Sciences'		,	'Int. J. Mol. Sci.'					,'IntJMolSci'	,[]	),
(	'International Journal of Quantum Chemistry'		,	'Int. J. Quantum Chem.'				,'IntJQChem'	,[]	),
(	'Journal of Applied Physics'						,	'J. Appl. Phys.'					,'JApplPhys'	,[]	),
(   'Journal of Catalysis'                              ,   'J. Catal.'                         ,'JCat'         ,[] ),
(	'Journal of Chemical Physics'						,	'J. Chem. Phys.'					,'JCP'			,[	'The Journal of chemical physics'				]	),
(	'Journal of Computational Chemistry'				,	'J. Comput. Chem.'					,'JCompChem'	,[]	),
(	'Journal of Experimental and Theoretical Physics'	,	'Zh. Eksp. Teor. Fiz.'				,'JETP'			,[]	),
(	'Journal of Luminescence'							,	'J. Lumin.'							,'JLum'			,[]	),
(	'Journal of Molecular Biology'						,	'J. Mol. Biol.'						,'JMolBio'		,[]	),
(	'Journal of Non-Crystalline Solids'					,	'J. Non-Cryst. Solids'				,'JNonCrystSolid',[] ),
(	'Journal of Nanotechnology'							,	'J. Nanotechnology'					,'JNanotech'	,[] ),
(	'Journal of Physics C: Solid State Physics'			,	'J. Phys. C: Solid State Phys.'		,'JPhysC'		,[]	),
(	'Journal of Physics: Condensed Matter'				,	'J. Phys.: Condens. Matter'			,'JPhysCondMat'	,[ 'Journal of physics. Condensed matter : an Institute of Physics journal' ]	),
(	'Journal of Physical Chemistry'						,	'J. Phys. Chem.'					,'JPC'			,[ 'The Journal of Physical Chemistry'			]	),
(	'Journal of Physical Chemistry A'					,	'J. Phys. Chem. A'					,'JPCa'			,[ 'The Journal of Physical Chemistry A'		]	),	
(	'Journal of Physical Chemistry B'					,	'J. Phys. Chem. B'					,'JPCb'			,[ 'The Journal of Physical Chemistry B'		]	),
(	'Journal of Physical Chemistry C'					,	'J. Phys. Chem. C'					,'JPCc'			,[ 'The Journal of Physical Chemistry C'		]	),
(	'Journal of Physical Chemistry Letters'				,	'J. Phys. Chem. Lett.'				,'JPCL'			,[ 'The Journal of Physical Chemistry Letters'	]	),
(	'Journal of the American Chemical Society'			,	'J. Am. Chem. Soc.'					,'JACS'			,[ 'JACS' ]	),
(	'Materials Science and Engineering A'				,	'Mater. Sci. Eng., A'				,'MatSciEngA'	,['Materials Science and Engineering: A'] ),
(	'Materials Science and Engineering B'				,	'Mater. Sci. Eng., B'				,'MatSciEngB'	,['Materials Science and Engineering: B'] ),
(	'Materials Science and Engineering C'				,	'Mater. Sci. Eng., C'				,'MatSciEngC'	,['Materials Science and Engineering: C'] ),
(	'Materials Science and Engineering Reports'			,	'Mater. Sci. Eng., R'				,'MatSciEngR'	,['Materials Science and Engineering: Reports'] ),
(	'Molecular Physics'									,	'Mol. Phys.'						,'MolPhys'		,[]	),
(	'Nano Letters'										,	'Nano Lett.'						,'NanoLett'		,[]	),
(	'Nano Research'										,	'Nano Res.'							,'NanoRes'		,[]	),
(	'Nanoscale'											,	'Nanoscale'							,'Nanoscale'	,[]	),
(	'Nanotechnology'									,	'Nanotechnology'					,'Nanotech'		,[]	),
(	'Nature'											,	'Nature'							,'Nat'			,[]	),
(	'Nature Chemistry'									,	'Nat. Chem.'						,'NatChem'		,[ 'Nature Chem.' ]	),
(	'Nature Materials'									,	'Nat. Mat.'							,'NatMat'		,[]	),
(	'Nature Nanotechnology'								,	'Nat. Nanotechnol.'					,'NatNano'		,[]	),
(	'Nature Physics'									,	'Nat. Phys.'						,'NatPhys'		,[]	),
(	'Nature Communications'								,	'Nat. Commun.'						,'NatCom'		,[]	),
(	'Nature Materials'									,	'Nat. Mater.'						,'NatMater'		,[]	),
(	'New Journal of Physics'							,	'New J. Phys.'						,'NewJPhys'		,[]	),
(   'Optics Express'                                    ,   'Opt. Express'                      ,'OptExp'       ,[] ),
(	'Organic Electronics'								,	'Org. Electron.'					,'OrgEl'		,[]	),
(	'Physica Status Solidi A'							,	'Phys. Status Solidi A'				,'PSSa'			,[ 'physica status solidi (a)'  ]	),
(	'Physica Status Solidi B'							,	'Phys. Status Solidi B'				,'PSSb'			,[ 'Physica Status Solidi (B)'  ]	),
(	'Physica Status Solidi C'							,	'Phys. Status Solidi C'				,'PSSc'			,[]	),
(	'Physica Status Solidi RRL'							,	'Phys. Status Solidi RRL'			,'PSSl'			,[]	),
(	'Physical Chemistry Chemical Physics'				,	'Phys. Chem. Chem. Phys.'			,'PCCP'			,[	'Phys Chem Chem Phys'	]	),
(	'Physical Review'									,	'Phys. Rev.'						,'PhysRev'		,[]	),
(	'Physical Review B'									,	'Phys. Rev. B'   					,'PhysRevB'		,[	'Phys. Rev.  B'	]	),
(	'Physical Review Letters'							,	'Phys. Rev. Lett.'					,'PhysRevLett'	,[]	),
(	'Reviews of Modern Physics'							,	'Rev. Mod. Phys.'					,'RevModPhys'	,[]	),
(	'Science'											,	'Science' 							,'Science' 		,[	'Science (New York, N.Y.)' ]	),
(	'Small'												, 	'Small'								,'Small' 		,[]	),
(	'Surface Science'									,	'Surf. Sci.'						,'SurfSci'		,[]	),
(   'Trends in plant science'							, 	'Trends Plant Sci.'					,'TrendPlantSci',[] ),
(	'Zeitschrift fur Physik'							,	'Z. Physik'							,'ZPhysik'		,[] )
]

