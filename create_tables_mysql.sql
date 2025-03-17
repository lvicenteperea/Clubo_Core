CREATE TABLE `_hissesbd` (
    `fechorfin` DATETIME NULL,
    `fechorini` DATETIME NOT NULL,
    `nompc` VARCHAR(40) NOT NULL,
    `nomapl` VARCHAR(60) NOT NULL,
    `PIDapl` INT NULL,
    `ruteje` VARCHAR(255) NOT NULL,
    `finfor` SMALLINT NOT NULL,
    `nomusu` VARCHAR(60) NULL,
    `verapl` VARCHAR(20) NULL,
    PRIMARY KEY (`fechorini` DATETIME NOT NULL, `nompc` VARCHAR(40) NOT NULL, `nomapl` VARCHAR(60) NOT NULL, `ruteje` VARCHAR(255) NOT NULL)
);

CREATE TABLE `_ver` (
    `ver` VARCHAR(10) NOT NULL,
    `numverint` INT NULL,
    `fechor` DATETIME NOT NULL,
    PRIMARY KEY (`ver` VARCHAR(10) NOT NULL)
);

CREATE TABLE `apa` (
    `codins` SMALLINT NOT NULL,
    `tip` SMALLINT NOT NULL,
    `num` SMALLINT NOT NULL,
    `nomcor` VARCHAR(20) NULL,
    `nomlar` VARCHAR(50) NULL,
    `dirip` VARCHAR(15) NULL,
    `datadi` VARCHAR(7168) NULL,
    `subtipapa` SMALLINT NULL,
    `nomcorviacer` VARCHAR(40) NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `tip` SMALLINT NOT NULL, `num` SMALLINT NOT NULL)
);

CREATE TABLE `apeman` (
    `codins` SMALLINT NOT NULL,
    `fechor` DATETIME NOT NULL,
    `horfechor` SMALLINT NOT NULL,
    `tipapa` SMALLINT NOT NULL,
    `numapa` SMALLINT NOT NULL,
    `tipape` SMALLINT NOT NULL,
    `fechorjus` DATETIME NULL,
    `codtipsop` SMALLINT NULL,
    `idepro` VARCHAR(20) NULL,
    `codinspro` SMALLINT NULL,
    `numpro` VARCHAR(12) NULL,
    `matrec` VARCHAR(12) NULL,
    `obs` VARCHAR(512) NULL,
    `codmot` SMALLINT NULL,
    `matasopro` VARCHAR(12) NULL,
    `fechorinc` DATETIME NULL,
    `horfechorinc` SMALLINT NULL,
    `codtipinc` SMALLINT NULL,
    `infvarinc` VARCHAR(256) NULL,
    `codope` SMALLINT NOT NULL,
    `codaut` SMALLINT NOT NULL,
    `codopejus` SMALLINT NULL,
    `numbar` SMALLINT NULL,
    `ideeve` VARCHAR(20) NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `fechor` DATETIME NOT NULL, `horfechor` SMALLINT NOT NULL, `tipapa` SMALLINT NOT NULL, `numapa` SMALLINT NOT NULL)
);

CREATE TABLE `c_condetcob` (
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(40) NOT NULL,
    `des_base` VARCHAR(40) NULL,
    `atr` VARCHAR(80) NULL,
    PRIMARY KEY (`cod` SMALLINT NOT NULL)
);

CREATE TABLE `c_contot` (
    `cod` SMALLINT NOT NULL,
    `sql` TEXT NOT NULL,
    `des` VARCHAR(128) NULL,
    `aplcajman` SMALLINT NOT NULL,
    `aplcajaut` SMALLINT NOT NULL,
    `atr` VARCHAR(80) NULL,
    PRIMARY KEY (`cod` SMALLINT NOT NULL)
);

CREATE TABLE `c_estpre` (
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(40) NOT NULL,
    `des_base` VARCHAR(40) NULL,
    `atr` VARCHAR(80) NULL,
    PRIMARY KEY (`cod` SMALLINT NOT NULL)
);

CREATE TABLE `c_forpag` (
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(40) NOT NULL,
    `des_base` VARCHAR(40) NULL,
    `atr` VARCHAR(80) NULL,
    PRIMARY KEY (`cod` SMALLINT NOT NULL)
);

CREATE TABLE `c_gruparcon` (
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(40) NOT NULL,
    `des_base` VARCHAR(40) NULL,
    PRIMARY KEY (`cod` SMALLINT NOT NULL)
);

CREATE TABLE `c_gruper` (
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(50) NULL,
    `des_base` VARCHAR(50) NULL,
    PRIMARY KEY (`cod` SMALLINT NOT NULL)
);

CREATE TABLE `c_ins` (
    `cod` SMALLINT NOT NULL,
    `nom` VARCHAR(60) NOT NULL,
    `nomfis` VARCHAR(60) NULL,
    `cif` VARCHAR(30) NULL,
    `dir` VARCHAR(120) NULL,
    `pob` VARCHAR(60) NULL,
    `pro` VARCHAR(40) NULL,
    `codpos` VARCHAR(5) NULL,
    `tel` VARCHAR(15) NULL,
    `totpla` SMALLINT NOT NULL,
    `dirfis` VARCHAR(120) NULL,
    `pobfis` VARCHAR(60) NULL,
    `profis` VARCHAR(40) NULL,
    `codposfis` VARCHAR(5) NULL,
    `datmerfac` VARCHAR(1024) NULL,
    `pai` VARCHAR(20) NULL,
    `paifis` VARCHAR(20) NULL,
    `codinsclo` SMALLINT NULL,
    `corele` VARCHAR(70) NULL,
    `infadi` VARCHAR(7168) NULL,
    `lat` FLOAT NULL,
    `lon` FLOAT NULL,
    `pagweb` VARCHAR(70) NULL,
    PRIMARY KEY (`cod` SMALLINT NOT NULL)
);

CREATE TABLE `c_parcon` (
    `nom` VARCHAR(60) NOT NULL,
    `codgruparcon` SMALLINT NOT NULL,
    `des` VARCHAR(128) NOT NULL,
    `valpordef` TEXT NOT NULL,
    `tipdat` VARCHAR(10) NULL,
    `domval` VARCHAR(256) NULL,
    `texexp` VARCHAR(512) NULL,
    PRIMARY KEY (`nom` VARCHAR(60) NOT NULL)
);

CREATE TABLE `c_per` (
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(80) NULL,
    `niv` SMALLINT NOT NULL,
    `codgruper` SMALLINT NOT NULL,
    `des_base` VARCHAR(80) NULL,
    `atr` VARCHAR(80) NULL,
    PRIMARY KEY (`cod` SMALLINT NOT NULL)
);

CREATE TABLE `c_resautpro` (
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(80) NOT NULL,
    `des_base` VARCHAR(80) NULL,
    `atr` VARCHAR(80) NULL,
    PRIMARY KEY (`cod` SMALLINT NOT NULL)
);

CREATE TABLE `c_subtipapa` (
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(30) NOT NULL,
    `des_base` VARCHAR(30) NULL,
    `atr` VARCHAR(80) NULL,
    PRIMARY KEY (`cod` SMALLINT NOT NULL)
);

CREATE TABLE `c_tipapa` (
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(30) NOT NULL,
    `des_base` VARCHAR(30) NULL,
    `atr` VARCHAR(80) NULL,
    PRIMARY KEY (`cod` SMALLINT NOT NULL)
);

CREATE TABLE `c_tipinc` (
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(80) NOT NULL,
    `des_base` VARCHAR(80) NULL,
    `atr` VARCHAR(80) NULL,
    PRIMARY KEY (`cod` SMALLINT NOT NULL)
);

CREATE TABLE `c_tipmanpro` (
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(80) NOT NULL,
    `tip` SMALLINT NULL,
    `des_base` VARCHAR(80) NULL,
    `atr` VARCHAR(80) NULL,
    PRIMARY KEY (`cod` SMALLINT NOT NULL)
);

CREATE TABLE `c_tipopeaud` (
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(80) NOT NULL,
    `des_base` VARCHAR(80) NULL,
    `atr` VARCHAR(80) NULL,
    PRIMARY KEY (`cod` SMALLINT NOT NULL)
);

CREATE TABLE `c_tipopecaj` (
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(80) NOT NULL,
    `des_base` VARCHAR(80) NULL,
    `atr` VARCHAR(80) NULL,
    PRIMARY KEY (`cod` SMALLINT NOT NULL)
);

CREATE TABLE `c_tippro` (
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(40) NOT NULL,
    `des_base` VARCHAR(40) NULL,
    `atr` VARCHAR(80) NULL,
    PRIMARY KEY (`cod` SMALLINT NOT NULL)
);

CREATE TABLE `c_tipsop` (
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(80) NOT NULL,
    `des_base` VARCHAR(80) NULL,
    `atr` VARCHAR(80) NULL,
    PRIMARY KEY (`cod` SMALLINT NOT NULL)
);

CREATE TABLE `camapa` (
    `codins` SMALLINT NOT NULL,
    `tipapa` SMALLINT NOT NULL,
    `numapa` SMALLINT NOT NULL,
    `tipapacam` SMALLINT NOT NULL,
    `numapacam` SMALLINT NOT NULL,
    `ord` SMALLINT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `tipapa` SMALLINT NOT NULL, `numapa` SMALLINT NOT NULL, `tipapacam` SMALLINT NOT NULL, `numapacam` SMALLINT NOT NULL)
);

CREATE TABLE `capima` (
    `codins` SMALLINT NOT NULL,
    `fechor` DATETIME NOT NULL,
    `horfechor` SMALLINT NOT NULL,
    `tipapa` SMALLINT NOT NULL,
    `numapa` SMALLINT NOT NULL,
    `numcam` SMALLINT NOT NULL,
    `rutcap` VARCHAR(128) NOT NULL,
    `tipopedis` INT NULL,
    `numpro` VARCHAR(12) NULL,
    `codrefope` VARCHAR(20) NULL,
    `mat` VARCHAR(12) NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `fechor` DATETIME NOT NULL, `horfechor` SMALLINT NOT NULL, `tipapa` SMALLINT NOT NULL, `numapa` SMALLINT NOT NULL, `numcam` SMALLINT NOT NULL)
);

CREATE TABLE `car` (
    `codins` SMALLINT NOT NULL,
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(40) NOT NULL,
    `expactcom` VARCHAR(128) NOT NULL,
    `tipapa` SMALLINT NOT NULL,
    `numapa` SMALLINT NOT NULL,
    `vis` SMALLINT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `cod` SMALLINT NOT NULL)
);

CREATE TABLE `cli` (
    `codins` SMALLINT NOT NULL,
    `cod` INT NOT NULL,
    `nom` VARCHAR(40) NULL,
    `ape` VARCHAR(60) NULL,
    `mos` VARCHAR(60) NULL,
    `nif` VARCHAR(30) NULL,
    `dom` VARCHAR(80) NULL,
    `pob` VARCHAR(50) NULL,
    `pro` VARCHAR(30) NULL,
    `codpos` VARCHAR(10) NULL,
    `tel1` VARCHAR(15) NULL,
    `tel2` VARCHAR(15) NULL,
    `obs` VARCHAR(256) NULL,
    `fecalt` DATETIME NULL,
    `fecbaj` DATETIME NULL,
    `maxtarpre` SMALLINT NULL,
    `impfia` FLOAT NULL,
    `codforpag` SMALLINT NULL,
    `numcue` VARCHAR(30) NULL,
    `emp` SMALLINT NULL,
    `txtmenrec` VARCHAR(128) NULL,
    `modmenrec` SMALLINT NULL,
    `vismenrec` SMALLINT NULL,
    `entsolprocli` SMALLINT NULL,
    `pai` VARCHAR(30) NULL,
    `corele` VARCHAR(60) NULL,
    `telmov` VARCHAR(15) NULL,
    `eve` SMALLINT NULL,
    `cuppro` SMALLINT NULL,
    `numplaasi` VARCHAR(40) NULL,
    `fecnac` VARCHAR(10) NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `cod` INT NOT NULL)
);

CREATE TABLE `cligrucli` (
    `codins` SMALLINT NOT NULL,
    `codcli` INT NOT NULL,
    `codinsgrucli` SMALLINT NOT NULL,
    `codgrucli` SMALLINT NOT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `codcli` INT NOT NULL, `codinsgrucli` SMALLINT NOT NULL, `codgrucli` SMALLINT NOT NULL)
);

CREATE TABLE `cob` (
    `codins` SMALLINT NOT NULL,
    `cod` VARCHAR(20) NOT NULL,
    `fechor` DATETIME NOT NULL,
    `horfechor` SMALLINT NOT NULL,
    `tipapa` SMALLINT NOT NULL,
    `numapa` SMALLINT NOT NULL,
    `codtur` VARCHAR(12) NOT NULL,
    `imptot` FLOAT NOT NULL,
    `porimp` FLOAT NOT NULL,
    `codforpag` SMALLINT NOT NULL,
    `impent` FLOAT NULL,
    `obs` VARCHAR(768) NULL,
    `solcop` SMALLINT NOT NULL,
    `codinscliaso` SMALLINT NULL,
    `codcliaso` INT NULL,
    `codope` SMALLINT NULL,
    `fechorret` DATETIME NULL,
    `pagsal` SMALLINT NULL,
    `num` INT NOT NULL,
    `numremrecdom` INT NULL,
    `codopecajaso` VARCHAR(20) NULL,
    `nomrazsoc` VARCHAR(60) NULL,
    `nif` VARCHAR(30) NULL,
    `domsoc` VARCHAR(80) NULL,
    `porimp2` FLOAT NULL,
    `porimp3` FLOAT NULL,
    `cuaultdigtarcre` VARCHAR(4) NULL,
    `numopetarcre` INT NULL,
    `numtratarcre` VARCHAR(15) NULL,
    `codcobaso` VARCHAR(20) NULL,
    `fircobsaftpt` VARCHAR(256) NULL,
    `codfac` VARCHAR(20) NULL,
    `reccob` TEXT NULL,
    `recemv` TEXT NULL,
    `ser` VARCHAR(7) NULL,
    `fircob` VARCHAR(8) NULL,
    `basimp` FLOAT NULL,
    `impimp` FLOAT NULL,
    `nomimp` VARCHAR(12) NULL,
    `nomimp2` VARCHAR(12) NULL,
    `nomimp3` VARCHAR(12) NULL,
    `tipdoc` VARCHAR(1) NULL,
    `codcobabo` VARCHAR(20) NULL,
    `codcobfac` VARCHAR(20) NULL,
    `ubiveh` VARCHAR(60) NULL,
    `codrefext` VARCHAR(32) NULL,
    `ideeve` VARCHAR(20) NULL,
    `ideage` VARCHAR(16) NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `cod` VARCHAR(20) NOT NULL)
);

CREATE TABLE `comeve` (
    `codins` SMALLINT NOT NULL,
    `ideeve` VARCHAR(60) NOT NULL,
    `fechor` DATETIME NOT NULL,
    `datadi` VARCHAR(512) NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `ideeve` VARCHAR(60) NOT NULL)
);

CREATE TABLE `con` (
    `codins` SMALLINT NOT NULL,
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(50) NOT NULL,
    `inttiereg` DATETIME NULL,
    `expval` VARCHAR(128) NULL,
    `selsqlval` VARCHAR(2048) NULL,
    `vissin` SMALLINT NULL,
    `valrefmin` SMALLINT NULL,
    `valrefmax` SMALLINT NULL,
    `vis` SMALLINT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `cod` SMALLINT NOT NULL)
);

CREATE TABLE `decperope` (
    `codins` SMALLINT NOT NULL,
    `codope` SMALLINT NOT NULL,
    `codper` SMALLINT NOT NULL,
    `acc` SMALLINT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `codope` SMALLINT NOT NULL, `codper` SMALLINT NOT NULL)
);

CREATE TABLE `detcob` (
    `codins` SMALLINT NOT NULL,
    `codcob` VARCHAR(20) NOT NULL,
    `ord` SMALLINT NOT NULL,
    `codtipcon` SMALLINT NOT NULL,
    `can` INT NOT NULL,
    `tie` DATETIME NOT NULL,
    `imp` FLOAT NOT NULL,
    `tietot` DATETIME NOT NULL,
    `imptot` FLOAT NOT NULL,
    `codtipsop` SMALLINT NULL,
    `idepro` VARCHAR(20) NULL,
    `codinspro` SMALLINT NULL,
    `numpro` VARCHAR(12) NULL,
    `codgrupro` SMALLINT NULL,
    `entest` DATETIME NULL,
    `pagest` DATETIME NULL,
    `codtar` SMALLINT NULL,
    `mat` VARCHAR(12) NULL,
    `exp` SMALLINT NOT NULL,
    `verpro` SMALLINT NULL,
    `codinscli` SMALLINT NULL,
    `codcli` INT NULL,
    `mos` VARCHAR(60) NULL,
    `salcon` FLOAT NULL,
    `saldis` FLOAT NULL,
    `codrefext` VARCHAR(32) NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `codcob` VARCHAR(20) NOT NULL, `ord` SMALLINT NOT NULL)
);

CREATE TABLE `detopecaj` (
    `codins` SMALLINT NOT NULL,
    `codopecaj` VARCHAR(20) NOT NULL,
    `ele` VARCHAR(20) NOT NULL,
    `valent` INT NULL,
    `valnum` FLOAT NULL,
    `valcad` VARCHAR(60) NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `codopecaj` VARCHAR(20) NOT NULL, `ele` VARCHAR(20) NOT NULL)
);

CREATE TABLE `entsal` (
    `codins` SMALLINT NOT NULL,
    `fechor` DATETIME NOT NULL,
    `horfechor` SMALLINT NOT NULL,
    `tipapa` SMALLINT NOT NULL,
    `numapa` SMALLINT NOT NULL,
    `codtipsop` SMALLINT NOT NULL,
    `idepro` VARCHAR(20) NOT NULL,
    `codinspro` SMALLINT NOT NULL,
    `numpro` VARCHAR(12) NOT NULL,
    `codgrupro` SMALLINT NOT NULL,
    `verpro` SMALLINT NOT NULL,
    `estpreant` SMALLINT NOT NULL,
    `nueestpre` SMALLINT NOT NULL,
    `codzonincplalib` SMALLINT NULL,
    `codzondecplalib` SMALLINT NULL,
    `matasopro` VARCHAR(12) NULL,
    `rutcapmat` VARCHAR(128) NULL,
    `tie` DATETIME NULL,
    `imp` FLOAT NULL,
    `fechorret` DATETIME NULL,
    `matrec` VARCHAR(12) NULL,
    `esalt` SMALLINT NOT NULL,
    `esbaj` SMALLINT NOT NULL,
    `indsobocu` SMALLINT NULL,
    `ord` INT NULL,
    `anu` SMALLINT NULL,
    `imppencob` FLOAT NULL,
    `codcobpen` VARCHAR(20) NULL,
    `codtardes` SMALLINT NULL,
    `salcon` FLOAT NULL,
    `saldis` FLOAT NULL,
    `accautmat` SMALLINT NULL,
    `codrefext` VARCHAR(32) NULL,
    `ideeve` VARCHAR(20) NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `fechor` DATETIME NOT NULL, `horfechor` SMALLINT NOT NULL, `tipapa` SMALLINT NOT NULL, `numapa` SMALLINT NOT NULL, `codtipsop` SMALLINT NOT NULL, `idepro` VARCHAR(20) NOT NULL, `verpro` SMALLINT NOT NULL)
);

CREATE TABLE `enu` (
    `codins` SMALLINT NOT NULL,
    `cod` VARCHAR(60) NOT NULL,
    `val` INT NOT NULL,
    `fechormod` DATETIME NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `cod` VARCHAR(60) NOT NULL)
);

CREATE TABLE `envinc` (
    `codins` SMALLINT NOT NULL,
    `codtipinc` SMALLINT NOT NULL,
    `des` VARCHAR(1024) NOT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `codtipinc` SMALLINT NOT NULL)
);

CREATE TABLE `equgruproins` (
    `codins` SMALLINT NOT NULL,
    `codinsaje` SMALLINT NOT NULL,
    `codgruproaje` SMALLINT NOT NULL,
    `codgrupro` SMALLINT NOT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `codinsaje` SMALLINT NOT NULL, `codgruproaje` SMALLINT NOT NULL)
);

CREATE TABLE `fac` (
    `codins` SMALLINT NOT NULL,
    `cod` VARCHAR(20) NOT NULL,
    `codcob` VARCHAR(20) NOT NULL,
    `fechor` DATETIME NOT NULL,
    `codope` SMALLINT NOT NULL,
    `codinscli` SMALLINT NULL,
    `codcli` INT NULL,
    `nomrazsoc` VARCHAR(60) NULL,
    `nif` VARCHAR(30) NULL,
    `docsoc` VARCHAR(80) NULL,
    `datcliadi` VARCHAR(512) NULL,
    `imptot` FLOAT NULL,
    `codforpag` SMALLINT NULL,
    `obs` VARCHAR(768) NULL,
    `pag` TEXT NULL,
    `fechorimp` DATETIME NULL,
    `fechorpag` DATETIME NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `cod` VARCHAR(20) NOT NULL)
);

CREATE TABLE `fes` (
    `codins` SMALLINT NOT NULL,
    `dia` SMALLINT NOT NULL,
    `mes` SMALLINT NOT NULL,
    `nom` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `dia` SMALLINT NOT NULL, `mes` SMALLINT NOT NULL)
);

CREATE TABLE `frahor` (
    `codins` SMALLINT NOT NULL,
    `codhor` SMALLINT NOT NULL,
    `num` SMALLINT NOT NULL,
    `dia` SMALLINT NULL,
    `ini` DATETIME NULL,
    `fin` DATETIME NULL,
    `estmax` DATETIME NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `codhor` SMALLINT NOT NULL, `num` SMALLINT NOT NULL)
);

CREATE TABLE `fratar` (
    `codins` SMALLINT NOT NULL,
    `codtar` SMALLINT NOT NULL,
    `num` INT NOT NULL,
    `dia` SMALLINT NOT NULL,
    `ini` DATETIME NOT NULL,
    `fin` DATETIME NOT NULL,
    `codlispre` SMALLINT NOT NULL,
    `entfra` SMALLINT NULL,
    `pagfra` SMALLINT NULL,
    `perfra` SMALLINT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `codtar` SMALLINT NOT NULL, `num` INT NOT NULL)
);

CREATE TABLE `grucli` (
    `codins` SMALLINT NOT NULL,
    `cod` SMALLINT NOT NULL,
    `nom` VARCHAR(50) NULL,
    `des` VARCHAR(128) NULL,
    `ord` INT NOT NULL,
    `col` VARCHAR(9) NOT NULL,
    `inirannum` INT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `cod` SMALLINT NOT NULL)
);

CREATE TABLE `grupro` (
    `codins` SMALLINT NOT NULL,
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(60) NOT NULL,
    `codtippro` SMALLINT NOT NULL,
    `tipapapro` SMALLINT NOT NULL,
    `nivpromin` SMALLINT NULL,
    `codtipsop` SMALLINT NOT NULL,
    `rannumdes` INT NOT NULL,
    `rannumhas` INT NOT NULL,
    `teximppro` VARCHAR(2048) NULL,
    `teximpval` VARCHAR(2048) NULL,
    `teximpcan` VARCHAR(2048) NULL,
    `cadpro` DATETIME NULL,
    `cadsopdef` SMALLINT NULL,
    `codhor` SMALLINT NULL,
    `entfuehor` SMALLINT NULL,
    `codtar` SMALLINT NULL,
    `tipcontraren` SMALLINT NULL,
    `entfuetraren` SMALLINT NULL,
    `codtarfuetraren` SMALLINT NULL,
    `diacorpagren` SMALLINT NULL,
    `diaantcrerenaut` SMALLINT NULL,
    `salrec` SMALLINT NULL,
    `codrecsalini` SMALLINT NULL,
    `valtie` DATETIME NULL,
    `valimp` FLOAT NULL,
    `valpor` SMALLINT NULL,
    `numusomaxdia` SMALLINT NULL,
    `numusotot` SMALLINT NULL,
    `cos` FLOAT NULL,
    `codinscli` SMALLINT NULL,
    `codcli` INT NULL,
    `cliedi` SMALLINT NULL,
    `modcobexc` SMALLINT NULL,
    `promarpag` SMALLINT NULL,
    `mosopcbuscaj` SMALLINT NULL,
    `icomos` SMALLINT NULL,
    `usoentsinmat` SMALLINT NULL,
    `usosalsinmat` SMALLINT NULL,
    `altsinmat` SMALLINT NULL,
    `fecinival` DATETIME NULL,
    `horinival` DATETIME NULL,
    `fecfinval` DATETIME NULL,
    `horfinval` DATETIME NULL,
    `regsop` SMALLINT NULL,
    `camedival` SMALLINT NULL,
    `camdifval` SMALLINT NULL,
    `dismaxcommat` SMALLINT NULL,
    `tiepas` SMALLINT NULL,
    `tiegra` SMALLINT NULL,
    `codzonaso` SMALLINT NULL,
    `cosvar` SMALLINT NULL,
    `tipbonsal` SMALLINT NULL,
    `apbdef` SMALLINT NULL,
    `impminapldes` FLOAT NULL,
    `saliniestlim` FLOAT NULL,
    `medconestlim` SMALLINT NULL,
    `perestlim` SMALLINT NULL,
    `dessalmin` FLOAT NULL,
    `dessalmax` FLOAT NULL,
    `tiegrabonsal` SMALLINT NULL,
    `codtarcos` SMALLINT NULL,
    `codtarrepag` SMALLINT NULL,
    `vis` SMALLINT NULL,
    `usoautmatpordef` SMALLINT NULL,
    `denexptic` SMALLINT NULL,
    `masbitselexp` INT NULL,
    `valcomselexp` INT NULL,
    `codgruproalt` SMALLINT NULL,
    `conadi` VARCHAR(2048) NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `cod` SMALLINT NOT NULL)
);

CREATE TABLE `hor` (
    `codins` SMALLINT NOT NULL,
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `cod` SMALLINT NOT NULL)
);

CREATE TABLE `inc` (
    `codins` SMALLINT NOT NULL,
    `fechor` DATETIME NOT NULL,
    `horfechor` SMALLINT NOT NULL,
    `tipapa` SMALLINT NOT NULL,
    `numapa` SMALLINT NOT NULL,
    `codtipinc` SMALLINT NOT NULL,
    `infvar` VARCHAR(256) NULL,
    `codtipsop` SMALLINT NULL,
    `idepro` VARCHAR(20) NULL,
    `codinspro` SMALLINT NULL,
    `numpro` VARCHAR(12) NULL,
    `codgrupro` SMALLINT NULL,
    `indestpag` SMALLINT NULL,
    `matasopro` VARCHAR(12) NULL,
    `matrec` VARCHAR(12) NULL,
    `tie` DATETIME NULL,
    `imp` FLOAT NULL,
    `codope` SMALLINT NULL,
    `tipaparel` SMALLINT NULL,
    `numaparel` SMALLINT NULL,
    `fechorret` DATETIME NULL,
    `fechormod` DATETIME NOT NULL,
    `verpro` SMALLINT NULL,
    `codinscli` SMALLINT NULL,
    `codcli` INT NULL,
    `resautrel` SMALLINT NULL,
    `ideeve` VARCHAR(20) NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `fechor` DATETIME NOT NULL, `horfechor` SMALLINT NOT NULL, `tipapa` SMALLINT NOT NULL, `numapa` SMALLINT NOT NULL, `codtipinc` SMALLINT NOT NULL)
);

CREATE TABLE `inssis` (
    `codins` SMALLINT NOT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL)
);

CREATE TABLE `lisnegmat` (
    `codins` SMALLINT NOT NULL,
    `mat` VARCHAR(12) NOT NULL,
    `obs` VARCHAR(250) NULL,
    `codope` SMALLINT NOT NULL,
    `fechor` DATETIME NOT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `mat` VARCHAR(12) NOT NULL)
);

CREATE TABLE `lisnegpro` (
    `codtipsop` SMALLINT NOT NULL,
    `idepro` VARCHAR(20) NOT NULL,
    `codinspro` SMALLINT NOT NULL,
    `numpro` VARCHAR(12) NOT NULL,
    `obs` VARCHAR(250) NULL,
    `codins` SMALLINT NOT NULL,
    `codope` SMALLINT NULL,
    `fechor` DATETIME NOT NULL,
    PRIMARY KEY (`codtipsop` SMALLINT NOT NULL, `idepro` VARCHAR(20) NOT NULL)
);

CREATE TABLE `lispre` (
    `codins` SMALLINT NOT NULL,
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(40) NOT NULL,
    `tiecor` DATETIME NOT NULL,
    `tiereg` DATETIME NOT NULL,
    `red` FLOAT NULL,
    `tipred` SMALLINT NULL,
    `tiecic` DATETIME NOT NULL,
    `codlispresigcic` SMALLINT NULL,
    `numpasrep` SMALLINT NULL,
    `impmax` FLOAT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `cod` SMALLINT NOT NULL)
);

CREATE TABLE `manpro` (
    `codins` SMALLINT NOT NULL,
    `fechor` DATETIME NOT NULL,
    `horfechor` SMALLINT NOT NULL,
    `tipapa` SMALLINT NOT NULL,
    `numapa` SMALLINT NOT NULL,
    `codtipsop` SMALLINT NOT NULL,
    `idepro` VARCHAR(20) NOT NULL,
    `codtipmanpro` SMALLINT NOT NULL,
    `codinspro` SMALLINT NOT NULL,
    `numpro` VARCHAR(12) NOT NULL,
    `codgrupro` SMALLINT NOT NULL,
    `verpro` SMALLINT NOT NULL,
    `codtur` VARCHAR(12) NULL,
    `codope` SMALLINT NULL,
    `codtipsopprovin` SMALLINT NULL,
    `ideproprovin` VARCHAR(20) NULL,
    `cadsop` DATETIME NULL,
    `blo` SMALLINT NULL,
    `inival` DATETIME NULL,
    `finval` DATETIME NULL,
    `estpre` SMALLINT NULL,
    `indestpag` SMALLINT NULL,
    `mat` VARCHAR(12) NULL,
    `obs` VARCHAR(128) NULL,
    `usoautmat` SMALLINT NULL,
    `nomtit` VARCHAR(40) NULL,
    `apetit` VARCHAR(60) NULL,
    `niftit` VARCHAR(30) NULL,
    `mos` VARCHAR(60) NULL,
    `ultmov` DATETIME NULL,
    `horultmov` SMALLINT NULL,
    `codcob` VARCHAR(20) NULL,
    `orddetcob` SMALLINT NULL,
    `codinscli` SMALLINT NULL,
    `codcli` INT NULL,
    `apb` SMALLINT NULL,
    `matultmov` VARCHAR(12) NULL,
    `infvar` VARCHAR(256) NULL,
    `omicommatent` SMALLINT NULL,
    `omicommatsal` SMALLINT NULL,
    `persobocu` SMALLINT NULL,
    `matsobocu` VARCHAR(12) NULL,
    `fechorentsobocu` DATETIME NULL,
    `numpla` VARCHAR(10) NULL,
    `imppencob` FLOAT NULL,
    `codcobpen` VARCHAR(20) NULL,
    `saldis` FLOAT NULL,
    `forcodtar` SMALLINT NULL,
    `ideeve` VARCHAR(20) NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `fechor` DATETIME NOT NULL, `horfechor` SMALLINT NOT NULL, `tipapa` SMALLINT NOT NULL, `numapa` SMALLINT NOT NULL, `codtipsop` SMALLINT NOT NULL, `idepro` VARCHAR(20) NOT NULL, `codtipmanpro` SMALLINT NOT NULL, `verpro` SMALLINT NOT NULL)
);

CREATE TABLE `ope` (
    `codins` SMALLINT NOT NULL,
    `cod` SMALLINT NOT NULL,
    `nom` VARCHAR(20) NOT NULL,
    `con` VARCHAR(40) NULL,
    `blo` SMALLINT NOT NULL,
    `nomcom` VARCHAR(60) NULL,
    `nif` VARCHAR(30) NULL,
    `dom` VARCHAR(80) NULL,
    `tel` VARCHAR(20) NULL,
    `codpos` VARCHAR(5) NULL,
    `pob` VARCHAR(30) NULL,
    `pro` VARCHAR(25) NULL,
    `nivpro` SMALLINT NOT NULL,
    `intaccfal` SMALLINT NULL,
    `fecultcamcon` DATETIME NULL,
    `nopuecamcon` SMALLINT NULL,
    `fechorultacc` DATETIME NULL,
    `exicamcon` SMALLINT NULL,
    `connuncad` SMALLINT NULL,
    `corele` VARCHAR(80) NULL,
    `telmov` VARCHAR(20) NULL,
    `fecalt` DATETIME NULL,
    `esgru` SMALLINT NULL,
    `codopeherper` SMALLINT NULL,
    `hiscon` VARCHAR(512) NULL,
    `inival` DATETIME NULL,
    `finval` DATETIME NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `cod` SMALLINT NOT NULL)
);

CREATE TABLE `opecaj` (
    `codins` SMALLINT NOT NULL,
    `cod` VARCHAR(20) NOT NULL,
    `fechor` DATETIME NOT NULL,
    `tipapa` SMALLINT NOT NULL,
    `numapa` SMALLINT NOT NULL,
    `codtur` VARCHAR(12) NOT NULL,
    `codtipopecaj` SMALLINT NOT NULL,
    `codope` SMALLINT NULL,
    `num` INT NOT NULL,
    `imptot` FLOAT NOT NULL,
    `con` VARCHAR(60) NULL,
    `codforpag` SMALLINT NOT NULL,
    `tir` TEXT NULL,
    `codinscliaso` SMALLINT NULL,
    `codcliaso` INT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `cod` VARCHAR(20) NOT NULL)
);

CREATE TABLE `opetarcre` (
    `codins` SMALLINT NOT NULL,
    `num` INT NOT NULL,
    `numremtarcre` INT NULL,
    `fechor` DATETIME NOT NULL,
    `tipapa` SMALLINT NOT NULL,
    `numapa` SMALLINT NOT NULL,
    `tipope` SMALLINT NOT NULL,
    `codcob` VARCHAR(20) NULL,
    `numtarcre` VARCHAR(38) NOT NULL,
    `cadtar` DATETIME NOT NULL,
    `pis2` VARCHAR(74) NULL,
    `imp` FLOAT NOT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `num` INT NOT NULL)
);

CREATE TABLE `parcon` (
    `codins` SMALLINT NOT NULL,
    `nom` VARCHAR(60) NOT NULL,
    `val` TEXT NOT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `nom` VARCHAR(60) NOT NULL)
);

CREATE TABLE `paslispre` (
    `codins` SMALLINT NOT NULL,
    `codlispre` SMALLINT NOT NULL,
    `num` SMALLINT NOT NULL,
    `dur` DATETIME NULL,
    `imp` FLOAT NULL,
    `maxdur` DATETIME NULL,
    `maximp` FLOAT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `codlispre` SMALLINT NOT NULL, `num` SMALLINT NOT NULL)
);

CREATE TABLE `perope` (
    `codins` SMALLINT NOT NULL,
    `codope` SMALLINT NOT NULL,
    `codper` SMALLINT NOT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `codope` SMALLINT NOT NULL, `codper` SMALLINT NOT NULL)
);

CREATE TABLE `plazon` (
    `codins` SMALLINT NOT NULL,
    `cod` SMALLINT NOT NULL,
    `pla` SMALLINT NOT NULL,
    `plaocu` SMALLINT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `cod` SMALLINT NOT NULL)
);

CREATE TABLE `polacc` (
    `codins` SMALLINT NOT NULL,
    `codgrupro` SMALLINT NOT NULL,
    `tipapa` SMALLINT NOT NULL,
    `numapa` SMALLINT NOT NULL,
    `expaut` VARCHAR(80) NOT NULL,
    `numbar` SMALLINT NULL,
    `codzonincplalib` SMALLINT NULL,
    `codzondecplalib` SMALLINT NULL,
    `estpreesp` SMALLINT NOT NULL,
    `nueestpre` SMALLINT NOT NULL,
    `acc` SMALLINT NOT NULL,
    `resautexpautneg` SMALLINT NOT NULL,
    `forcodtar` SMALLINT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `codgrupro` SMALLINT NOT NULL, `tipapa` SMALLINT NOT NULL, `numapa` SMALLINT NOT NULL)
);

CREATE TABLE `proencir` (
    `codtipsop` SMALLINT NOT NULL,
    `idepro` VARCHAR(20) NOT NULL,
    `codinspro` SMALLINT NOT NULL,
    `numpro` VARCHAR(12) NOT NULL,
    `codgrupro` SMALLINT NOT NULL,
    `numapapro` SMALLINT NULL,
    `ord` INT NULL,
    `codtipsopprovin` SMALLINT NULL,
    `ideproprovin` VARCHAR(20) NULL,
    `ultmov` DATETIME NULL,
    `horultmov` SMALLINT NULL,
    `codinsultmov` SMALLINT NULL,
    `tipapaultmov` SMALLINT NULL,
    `numapaultmov` SMALLINT NULL,
    `cadsop` DATETIME NULL,
    `blo` SMALLINT NOT NULL,
    `inival` DATETIME NULL,
    `finval` DATETIME NULL,
    `estpre` SMALLINT NULL,
    `indestpag` SMALLINT NULL,
    `mat` VARCHAR(12) NULL,
    `codinscli` SMALLINT NULL,
    `codcli` INT NULL,
    `obs` VARCHAR(128) NULL,
    `usoautmat` SMALLINT NULL,
    `idetaraboant` VARCHAR(20) NULL,
    `fechorultgra` DATETIME NULL,
    `congra` SMALLINT NULL,
    `nomtit` VARCHAR(40) NULL,
    `apetit` VARCHAR(60) NULL,
    `niftit` VARCHAR(30) NULL,
    `mos` VARCHAR(60) NULL,
    `fechormod` DATETIME NOT NULL,
    `conpagren` SMALLINT NULL,
    `verpro` SMALLINT NOT NULL,
    `apb` SMALLINT NOT NULL,
    `matultmov` VARCHAR(12) NULL,
    `omicommatent` SMALLINT NULL,
    `omicommatsal` SMALLINT NULL,
    `persobocu` SMALLINT NULL,
    `matsobocu` VARCHAR(12) NULL,
    `fechorentsobocu` DATETIME NULL,
    `numpla` VARCHAR(10) NULL,
    `fechorlimvis` DATETIME NULL,
    `notuso` SMALLINT NULL,
    `fechorultrenaut` DATETIME NULL,
    `rutcapmat` VARCHAR(128) NULL,
    `conuso` INT NULL,
    `fecalt` DATETIME NULL,
    `saldis` FLOAT NULL,
    `datadi` VARCHAR(2048) NULL,
    `ultcodzoninc` SMALLINT NULL,
    `ultcodzondec` SMALLINT NULL,
    `forcodtar` SMALLINT NULL,
    `codgruprovin1` SMALLINT NULL,
    `codgruprovin2` SMALLINT NULL,
    `codgruprovin3` SMALLINT NULL,
    `codgruprovin4` SMALLINT NULL,
    `fechorent` DATETIME NULL,
    `fechorpag` DATETIME NULL,
    `fechorsal` DATETIME NULL,
    `fecbajcir` DATETIME NULL,
    `impentfia` FLOAT NULL,
    `desimpcob` FLOAT NULL,
    `desporcob` SMALLINT NULL,
    `destiecob` DATETIME NULL,
    `locres` VARCHAR(20) NULL,
    PRIMARY KEY (`codtipsop` SMALLINT NOT NULL, `idepro` VARCHAR(20) NOT NULL)
);

CREATE TABLE `profuecir` (
    `codtipsop` SMALLINT NOT NULL,
    `idepro` VARCHAR(20) NOT NULL,
    `codinspro` SMALLINT NOT NULL,
    `numpro` VARCHAR(12) NOT NULL,
    `codgrupro` SMALLINT NOT NULL,
    `numapapro` SMALLINT NULL,
    `ord` INT NULL,
    `codtipsopprovin` SMALLINT NULL,
    `ideproprovin` VARCHAR(20) NULL,
    `ultmov` DATETIME NULL,
    `horultmov` SMALLINT NULL,
    `codinsultmov` SMALLINT NULL,
    `tipapaultmov` SMALLINT NULL,
    `numapaultmov` SMALLINT NULL,
    `cadsop` DATETIME NULL,
    `blo` SMALLINT NOT NULL,
    `inival` DATETIME NULL,
    `finval` DATETIME NULL,
    `estpre` SMALLINT NULL,
    `indestpag` SMALLINT NULL,
    `mat` VARCHAR(12) NULL,
    `codinscli` SMALLINT NULL,
    `codcli` INT NULL,
    `obs` VARCHAR(128) NULL,
    `usoautmat` SMALLINT NULL,
    `idetaraboant` VARCHAR(20) NULL,
    `fechorultgra` DATETIME NULL,
    `congra` SMALLINT NULL,
    `nomtit` VARCHAR(40) NULL,
    `apetit` VARCHAR(60) NULL,
    `niftit` VARCHAR(30) NULL,
    `mos` VARCHAR(60) NULL,
    `fechormod` DATETIME NOT NULL,
    `conpagren` SMALLINT NULL,
    `verpro` SMALLINT NOT NULL,
    `apb` SMALLINT NOT NULL,
    `matultmov` VARCHAR(12) NULL,
    `omicommatent` SMALLINT NULL,
    `omicommatsal` SMALLINT NULL,
    `persobocu` SMALLINT NULL,
    `matsobocu` VARCHAR(12) NULL,
    `fechorentsobocu` DATETIME NULL,
    `numpla` VARCHAR(10) NULL,
    `fechorlimvis` DATETIME NULL,
    `notuso` SMALLINT NULL,
    `fechorultrenaut` DATETIME NULL,
    `rutcapmat` VARCHAR(128) NULL,
    `conuso` INT NULL,
    `fecalt` DATETIME NULL,
    `saldis` FLOAT NULL,
    `datadi` VARCHAR(2048) NULL,
    `ultcodzoninc` SMALLINT NULL,
    `ultcodzondec` SMALLINT NULL,
    `forcodtar` SMALLINT NULL,
    `codgruprovin1` SMALLINT NULL,
    `codgruprovin2` SMALLINT NULL,
    `codgruprovin3` SMALLINT NULL,
    `codgruprovin4` SMALLINT NULL,
    `fechorent` DATETIME NULL,
    `fechorpag` DATETIME NULL,
    `fechorsal` DATETIME NULL,
    `fecbajcir` DATETIME NULL,
    `impentfia` FLOAT NULL,
    `desimpcob` FLOAT NULL,
    `desporcob` SMALLINT NULL,
    `destiecob` DATETIME NULL,
    `locres` VARCHAR(20) NULL,
    PRIMARY KEY (`codtipsop` SMALLINT NOT NULL, `idepro` VARCHAR(20) NOT NULL, `verpro` SMALLINT NOT NULL)
);

CREATE TABLE `rec` (
    `codins` SMALLINT NOT NULL,
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(20) NULL,
    `impcob` FLOAT NOT NULL,
    `salrec` FLOAT NULL,
    `tip` SMALLINT NULL,
    `codgrupro` SMALLINT NULL,
    `aplcajman` SMALLINT NULL,
    `aplcajaut` SMALLINT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `cod` SMALLINT NOT NULL)
);

CREATE TABLE `regaud` (
    `codins` SMALLINT NOT NULL,
    `fechor` DATETIME NOT NULL,
    `horfechor` SMALLINT NOT NULL,
    `tipapa` SMALLINT NOT NULL,
    `numapa` SMALLINT NOT NULL,
    `codope` SMALLINT NOT NULL,
    `tipopeaud` SMALLINT NOT NULL,
    `modope` SMALLINT NULL,
    `codtipsop` SMALLINT NULL,
    `idepro` VARCHAR(20) NULL,
    `codinspro` SMALLINT NULL,
    `numpro` VARCHAR(12) NULL,
    `infvar` VARCHAR(512) NULL,
    `firreg` VARCHAR(8) NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `fechor` DATETIME NOT NULL, `horfechor` SMALLINT NOT NULL, `tipapa` SMALLINT NOT NULL, `numapa` SMALLINT NOT NULL, `codope` SMALLINT NOT NULL, `tipopeaud` SMALLINT NOT NULL)
);

CREATE TABLE `regcon` (
    `codins` SMALLINT NOT NULL,
    `fechor` DATETIME NOT NULL,
    `horfechor` SMALLINT NOT NULL,
    `codcon` SMALLINT NOT NULL,
    `valcon` SMALLINT NOT NULL,
    `numframedhor` SMALLINT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `fechor` DATETIME NOT NULL, `horfechor` SMALLINT NOT NULL, `codcon` SMALLINT NOT NULL)
);

CREATE TABLE `regpreusu` (
    `codins` SMALLINT NOT NULL,
    `nomusu` VARCHAR(60) NOT NULL,
    `nomcla` VARCHAR(256) NOT NULL,
    `nomval` VARCHAR(256) NOT NULL,
    `tipdat` VARCHAR(10) NOT NULL,
    `val` TEXT NOT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `nomusu` VARCHAR(60) NOT NULL, `nomcla` VARCHAR(256) NOT NULL, `nomval` VARCHAR(256) NOT NULL)
);

CREATE TABLE `remrecdom` (
    `codins` SMALLINT NOT NULL,
    `num` INT NOT NULL,
    `banrecent` VARCHAR(4) NOT NULL,
    `banrecofi` VARCHAR(4) NOT NULL,
    `fechor` DATETIME NOT NULL,
    `numope` INT NOT NULL,
    `imptot` FLOAT NULL,
    `feccar` DATETIME NOT NULL,
    `codope` SMALLINT NOT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `num` INT NOT NULL)
);

CREATE TABLE `remtarcre` (
    `codins` SMALLINT NOT NULL,
    `num` INT NOT NULL,
    `numcom` VARCHAR(9) NOT NULL,
    `fechor` DATETIME NOT NULL,
    `numope` INT NOT NULL,
    `imptot` FLOAT NULL,
    `codope` SMALLINT NOT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `num` INT NOT NULL)
);

CREATE TABLE `renpro` (
    `codins` SMALLINT NOT NULL,
    `codtipsop` SMALLINT NOT NULL,
    `idepro` VARCHAR(20) NOT NULL,
    `initra` DATETIME NOT NULL,
    `fintra` DATETIME NOT NULL,
    `des` VARCHAR(64) NULL,
    `imppencob` FLOAT NOT NULL,
    `codcobpen` VARCHAR(20) NULL,
    `codinstraren` SMALLINT NULL,
    `codtraren` SMALLINT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `codtipsop` SMALLINT NOT NULL, `idepro` VARCHAR(20) NOT NULL, `initra` DATETIME NOT NULL)
);

CREATE TABLE `res` (
    `codins` SMALLINT NOT NULL,
    `loc` VARCHAR(20) NOT NULL,
    `fechoralt` DATETIME NOT NULL,
    `mat` VARCHAR(12) NULL,
    `tippro` SMALLINT NOT NULL,
    `fechorini` DATETIME NOT NULL,
    `fechorfin` DATETIME NOT NULL,
    `nomtit` VARCHAR(60) NULL,
    `tel` VARCHAR(15) NULL,
    `corele` VARCHAR(60) NULL,
    `obs` VARCHAR(512) NULL,
    `ideref` VARCHAR(128) NULL,
    `impcob` FLOAT NULL,
    `usoautmat` SMALLINT NULL,
    `salini` FLOAT NULL,
    `gruprovin` SMALLINT NULL,
    `anu` SMALLINT NULL,
    `codinscli` SMALLINT NULL,
    `codcli` INT NULL,
    `codtipsop` SMALLINT NULL,
    `idepro` VARCHAR(20) NULL,
    `codgrupro` SMALLINT NULL,
    `numpro` VARCHAR(12) NULL,
    `codbarpro` VARCHAR(128) NULL,
    `clapinpad` VARCHAR(8) NULL,
    `usudig` VARCHAR(40) NULL,
    `idusudig` INT NULL,
    `plaasi` VARCHAR(16) NULL,
    `fechoruso` DATETIME NULL,
    `ideage` VARCHAR(16) NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `loc` VARCHAR(20) NOT NULL)
);

CREATE TABLE `tar` (
    `codins` SMALLINT NOT NULL,
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(40) NOT NULL,
    `codlispredef` SMALLINT NULL,
    `limimp24h` FLOAT NULL,
    `codtarconaut` SMALLINT NULL,
    `fechorinicontar` DATETIME NULL,
    `fechorfincontar` DATETIME NULL,
    `tip` SMALLINT NOT NULL,
    `impfij` FLOAT NULL,
    `vis` SMALLINT NULL,
    `tiecor` DATETIME NULL,
    `tiereg` DATETIME NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `cod` SMALLINT NOT NULL)
);

CREATE TABLE `tarpro` (
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(40) NOT NULL,
    `hab` SMALLINT NOT NULL,
    `fechorini` DATETIME NOT NULL,
    `frerep` DATETIME NOT NULL,
    `tipeje` SMALLINT NOT NULL,
    `ord` TEXT NOT NULL,
    `com` VARCHAR(256) NULL,
    `fechorulteje` DATETIME NULL,
    `ultres` VARCHAR(256) NULL,
    PRIMARY KEY (`cod` SMALLINT NOT NULL)
);

CREATE TABLE `tottur` (
    `codins` SMALLINT NOT NULL,
    `codtur` VARCHAR(12) NOT NULL,
    `codtot` VARCHAR(30) NOT NULL,
    `subcodtot` VARCHAR(15) NOT NULL,
    `totent` INT NULL,
    `totnum` FLOAT NULL,
    `tottie` DATETIME NULL,
    `totcad` VARCHAR(60) NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `codtur` VARCHAR(12) NOT NULL, `codtot` VARCHAR(30) NOT NULL, `subcodtot` VARCHAR(15) NOT NULL)
);

CREATE TABLE `traerrsis` (
    `fechor` DATETIME NOT NULL,
    `mod` VARCHAR(20) NOT NULL,
    `vermod` VARCHAR(10) NULL,
    `cla` VARCHAR(40) NULL,
    `des` VARCHAR(256) NULL
);

CREATE TABLE `traren` (
    `codins` SMALLINT NOT NULL,
    `cod` SMALLINT NOT NULL,
    `codgrupro` SMALLINT NULL,
    `des` VARCHAR(64) NULL,
    `plames` SMALLINT NULL,
    `pladia` SMALLINT NULL,
    `imp` FLOAT NULL,
    `codtarimp` SMALLINT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `cod` SMALLINT NOT NULL)
);

CREATE TABLE `tur` (
    `codins` SMALLINT NOT NULL,
    `cod` VARCHAR(12) NOT NULL,
    `num` INT NOT NULL,
    `fechorape` DATETIME NOT NULL,
    `fechorcie` DATETIME NULL,
    `tipapa` SMALLINT NOT NULL,
    `numapa` SMALLINT NOT NULL,
    `salini` FLOAT NOT NULL,
    `salfin` FLOAT NULL,
    `codopeape` SMALLINT NULL,
    `codopecie` SMALLINT NULL,
    `tir` TEXT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `cod` VARCHAR(12) NOT NULL)
);

CREATE TABLE `vehcli` (
    `codins` SMALLINT NOT NULL,
    `mat` VARCHAR(12) NOT NULL,
    `codinscli` SMALLINT NOT NULL,
    `codcli` INT NOT NULL,
    `matocr` VARCHAR(12) NULL,
    `mar` VARCHAR(20) NULL,
    `mod` VARCHAR(30) NULL,
    `col` VARCHAR(15) NULL,
    `obs` VARCHAR(64) NULL,
    `fechormod` DATETIME NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `mat` VARCHAR(12) NOT NULL)
);

CREATE TABLE `veropepro` (
    `codtipsop` SMALLINT NOT NULL,
    `idepro` VARCHAR(20) NOT NULL,
    `ver` SMALLINT NOT NULL,
    `fechormod` DATETIME NULL,
    PRIMARY KEY (`codtipsop` SMALLINT NOT NULL, `idepro` VARCHAR(20) NOT NULL)
);

CREATE TABLE `zon` (
    `codins` SMALLINT NOT NULL,
    `cod` SMALLINT NOT NULL,
    `des` VARCHAR(50) NOT NULL,
    `pla` SMALLINT NOT NULL,
    `vis` SMALLINT NULL,
    PRIMARY KEY (`codins` SMALLINT NOT NULL, `cod` SMALLINT NOT NULL)
);

