import os, sys
import pandas as pd
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QFileDialog
from PyQt5.QtWidgets import QPushButton, QRadioButton
from PyQt5.QtWidgets import QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox, QLineEdit, QTextEdit, QLabel
from PyQt5.QtWidgets import QStackedWidget, QGroupBox, QFrame, QTableWidget, QTreeWidget, QTreeWidgetItem, QListView
from PyQt5.QtWidgets import QFormLayout, QGridLayout, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QIcon, QPixmap

from data import Data

class App(QMainWindow):
    def __init__(self):
    	super().__init__()
    	self.leftPanel = QStackedWidget(self)
    	self.rightPanel = QGroupBox(self)
    	self.initUI()

    def __setLabel(self, str, parent, font=QFont()):
    	label = QLabel(str, parent)
    	label.setFont(font)
    	return label

    def __setSpinBox(self, val, min, max, stepsize, parent):
    	box = QSpinBox(parent)
    	box.setMinimum(min)
    	box.setMaximum(max)
    	box.setSingleStep(stepsize)
    	box.setValue(val)
    	return box

    def __setDoubleSpinBox(self, val, min, max, stepsize, prec, parent):
    	box = QDoubleSpinBox(parent)
    	box.setMinimum(min)
    	box.setMaximum(max)
    	box.setSingleStep(stepsize)
    	box.setValue(val)
    	box.setDecimals(prec)
    	return box

    def __openLabeledFile(self):
    	filepath = QFileDialog.getOpenFileName(self.dataPage, 'Select File...')
    	filepath = filepath[0]

    	if filepath is not '':
    		filename = os.path.basename(filepath)
    		self.labeledFileDisplay.setText(filename)
    		labeledDataFrame = pd.read_csv(filepath, delimiter=',')
    		self.labeledData = Data(labeledDataFrame, filename, True)
    		self.dataSummaryTree.takeTopLevelItem(0)
    		self.__printDataSummary(self.labeledData)
    		self.splitFrame.setEnabled(True)
    		self.validationFrame.setEnabled(True)
    		self.dataNextPushButton.setEnabled(True)

    def __openUnlabeledFile(self):
    	filepath = QFileDialog.getOpenFileName(self.dataPage, 'Select File...')
    	filepath = filepath[0]

    	if filepath is not '':
    		filename = os.path.basename(filepath)
    		self.unlabeledFileDisplay.setText(filename)
    		unlabeledDataFrame = pd.read_csv(filepath, delimiter=',')
    		self.unlabeledData = Data(unlabeledDataFrame, filename, False)
    		self.dataSummaryTree.takeTopLevelItem(1)
    		self.__printDataSummary(self.unlabeledData)
    		self.predictionPushButton.setEnabled(True)

    def __printDataSummary(self, data):
    	filename = QTreeWidgetItem(self.dataSummaryTree)
    	filename.setText(0, data.getName())
    	sample = QTreeWidgetItem(filename)
    	sample.setText(0, 'Samples')
    	sample.setText(1, str(data.getNumOfSamples()))
    	classCountDic = data.getClassCounts()
    	
    	for c in classCountDic:
    		classCount = QTreeWidgetItem(sample)
    		classCount.setText(0, c)
    		classCount.setText(1, str(classCountDic[c]))
    		classCount.setToolTip(0, c)

    	feature = QTreeWidgetItem(filename)
    	feature.setText(0, 'Features')
    	feature.setText(1, str(data.getNumOfFeatures()))
    	featureTypeDic = data.getTypeOfFeatures()

    	for f in featureTypeDic:
    		featureType = QTreeWidgetItem(feature)
    		featureType.setText(0, f)
    		featureType.setText(1, str(featureTypeDic[f]))
    		featureType.setToolTip(0, f)

    	return filename

    def initUI(self):
    	titleFont = QFont()
    	titleFont.setBold(True)
    	
    	
    	########## 1st page: data loading and splitting ##########
    	self.dataPage = QWidget()
    	openIcon = QIcon('icons/open.png')
    	dataPageLayout = QVBoxLayout(self.dataPage)

    	### load labeled data
    	labeledDataLabel = self.__setLabel('Labeled Data:', self.dataPage, titleFont)
    	labeledFilePushButton = QPushButton('Select File...', self.dataPage)
    	labeledFilePushButton.setIcon(openIcon)
    	labeledFilePushButton.setMaximumWidth(140)
    	labeledFileSpacer = QSpacerItem(40, 20)
    	self.labeledFileDisplay = QLabel('<filename>', self.dataPage)

    	dataPageLayout.addWidget(labeledDataLabel)
    	labeledFileLayout = QHBoxLayout()
    	labeledFileLayout.addWidget(labeledFilePushButton)
    	labeledFileLayout.addItem(labeledFileSpacer)
    	labeledFileLayout.addWidget(self.labeledFileDisplay)
    	dataPageLayout.addLayout(labeledFileLayout)

    	labeledFilePushButton.clicked.connect(self.__openLabeledFile)

    	### load unlabeled data
    	unlabeledDataLabel = self.__setLabel('Unlabeled Data:', self.dataPage, titleFont)
    	unlabeledFilePushButton = QPushButton('Select File...', self.dataPage)
    	unlabeledFilePushButton.setIcon(openIcon)
    	unlabeledFilePushButton.setMaximumWidth(140)
    	unlabeledFileSpacer = QSpacerItem(40, 20)
    	self.unlabeledFileDisplay = QLabel('<filename>', self.dataPage)

    	dataPageLayout.addWidget(unlabeledDataLabel)
    	unlabeledFileLayout = QHBoxLayout()
    	unlabeledFileLayout.addWidget(unlabeledFilePushButton)
    	unlabeledFileLayout.addItem(unlabeledFileSpacer)
    	unlabeledFileLayout.addWidget(self.unlabeledFileDisplay)
    	dataPageLayout.addLayout(unlabeledFileLayout)

    	unlabeledFilePushButton.clicked.connect(self.__openUnlabeledFile)

    	### data summary
    	dataSummaryLabel = self.__setLabel('Data Summary:', self.dataPage, titleFont)
    	self.dataSummaryTree = QTreeWidget(self.dataPage)
    	self.dataSummaryTree.setColumnCount(2)
    	self.dataSummaryTree.setHeaderHidden(True)
    	self.dataSummaryTree.setColumnWidth(0, 200)
    	dataPageLayout.addWidget(dataSummaryLabel)
    	dataPageLayout.addWidget(self.dataSummaryTree)

    	### train/test split
    	trainTestLabel = self.__setLabel('Train/Test Split:', self.dataPage, titleFont)
    	self.splitFrame = QFrame(self.dataPage)
    	self.splitFrame.setAutoFillBackground(True)
    	self.splitFrame.setDisabled(True)
    	splitSpinBox = self.__setSpinBox(20, 10, 50, 10, self.splitFrame)
    	splitSpinBox.setMaximumWidth(60)
    	splitLabel = self.__setLabel('% for test', self.splitFrame)
    	splitCheckBox = QCheckBox('Stratified Sampling', self.splitFrame)
    	splitCheckBox.setChecked(True)

    	dataPageLayout.addWidget(trainTestLabel)
    	trainTestLayout = QHBoxLayout()
    	trainTestLayout.addWidget(splitSpinBox)
    	trainTestLayout.addWidget(splitLabel)
    	trainTestLayout.addWidget(splitCheckBox)
    	splitLayout = QVBoxLayout(self.splitFrame)
    	splitLayout.addLayout(trainTestLayout)
    	dataPageLayout.addWidget(self.splitFrame)

    	### validation methodology
    	validationLabel = self.__setLabel('Validation Methodology:', self.dataPage, titleFont)
    	self.validationFrame = QFrame(self.dataPage)
    	self.validationFrame.setAutoFillBackground(True)
    	self.validationFrame.setDisabled(True)
    	holdoutRadioButton = QRadioButton('Holdout Validation', self.validationFrame)
    	cvRadioButton = QRadioButton('K-Fold Cross-Validation', self.validationFrame)
    	cvRadioButton.setChecked(True)
    	looRadioButton = QRadioButton('Leave-One-Out Validation', self.validationFrame)
    	holdoutSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    	cvSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    	looSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    	validationSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    	holdoutSpinBox = self.__setSpinBox(20, 10, 50, 10, self.validationFrame)
    	holdoutSpinBox.setMaximumWidth(50)
    	holdoutSpinBox.setDisabled(True)
    	cvSpinBox = self.__setSpinBox(10, 5, 20, 5, self.validationFrame)
    	validationCheckBox = QCheckBox('Stratified Sampling', self.validationFrame)
    	validationCheckBox.setChecked(True)
    	holdoutLabel = self.__setLabel('% for validation', self.validationFrame)
    	cvLabel = self.__setLabel('folds', self.validationFrame)

    	holdoutRadioButton.toggled.connect(holdoutSpinBox.setEnabled)
    	holdoutRadioButton.toggled.connect(cvSpinBox.setDisabled)
    	holdoutRadioButton.toggled.connect(validationCheckBox.setEnabled)
    	cvRadioButton.toggled.connect(holdoutSpinBox.setDisabled)
    	cvRadioButton.toggled.connect(cvSpinBox.setEnabled)
    	cvRadioButton.toggled.connect(validationCheckBox.setEnabled)
    	looRadioButton.toggled.connect(holdoutSpinBox.setDisabled)
    	looRadioButton.toggled.connect(cvSpinBox.setDisabled)
    	looRadioButton.toggled.connect(validationCheckBox.setDisabled)

    	dataPageLayout.addWidget(validationLabel)
    	holdoutLayout = QHBoxLayout()
    	holdoutLayout.addWidget(holdoutRadioButton)
    	holdoutLayout.addItem(holdoutSpacer)
    	holdoutLayout.addWidget(holdoutSpinBox)
    	holdoutLayout.addWidget(holdoutLabel)
    	cvLayout = QHBoxLayout()
    	cvLayout.addWidget(cvRadioButton)
    	cvLayout.addItem(cvSpacer)
    	cvLayout.addWidget(cvSpinBox)
    	cvLayout.addWidget(cvLabel)
    	looLayout = QHBoxLayout()
    	looLayout.addWidget(looRadioButton)
    	looLayout.addItem(looSpacer)
    	samplingLayout = QHBoxLayout()
    	samplingLayout.addItem(validationSpacer)
    	samplingLayout.addWidget(validationCheckBox)
    	validationLayout = QVBoxLayout(self.validationFrame)
    	validationLayout.addLayout(holdoutLayout)
    	validationLayout.addLayout(cvLayout)
    	validationLayout.addLayout(looLayout)
    	validationLayout.addLayout(samplingLayout)
    	dataPageLayout.addWidget(self.validationFrame)

    	### data spacer and line
    	dataSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
    	dataPageLayout.addItem(dataSpacer)
    	dataLine = QFrame(self.dataPage)
    	dataLine.setFrameShape(QFrame.HLine)
    	dataLine.setFrameShadow(QFrame.Sunken)
    	dataPageLayout.addWidget(dataLine)

    	### next button
    	dataNextSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    	self.dataNextPushButton = QPushButton('Next', self.dataPage)
    	self.dataNextPushButton.setDefault(True)
    	self.dataNextPushButton.setMinimumWidth(90)
    	self.dataNextPushButton.setDisabled(True)
    	self.dataNextPushButton.clicked.connect(lambda: self.leftPanel.setCurrentIndex(1))
    	dataNextLayout = QHBoxLayout()
    	dataNextLayout.addItem(dataNextSpacer)
    	dataNextLayout.addWidget(self.dataNextPushButton)
    	dataPageLayout.addLayout(dataNextLayout)

    	self.leftPanel.addWidget(self.dataPage)

    	
    	########## 2nd page: training ##########
    	
    	modelPage = QWidget()
    	modelPageLayout = QVBoxLayout(modelPage)

    	### classifier type
    	classTypeLabel = self.__setLabel('Classifier Type:', modelPage, titleFont)
    	classTypeComboBox = QComboBox(modelPage)
    	classTypeLayout = QHBoxLayout()
    	classTypeLayout.addWidget(classTypeLabel)
    	classTypeLayout.addWidget(classTypeComboBox)

    	### classifier parameter stack
    	paramStack = QStackedWidget(modelPage)
    	paramStack.setMinimumHeight(320)
    	classTypeComboBox.currentIndexChanged.connect(paramStack.setCurrentIndex)

    	modelPageLayout.addLayout(classTypeLayout)
    	modelPageLayout.addWidget(paramStack)

    	## initial empty page
    	noneIcon = QIcon('icons/none.png')
    	classTypeComboBox.addItem(noneIcon, '-- Select Classifier --')
    	initPage = QWidget()
    	paramStack.addWidget(initPage)

    	## decision tree
    	dtIcon = QIcon('icons/dt.png')
    	classTypeComboBox.addItem(dtIcon, 'Decision Tree')
    	dtPage = QWidget()
    	paramStack.addWidget(dtPage)

    	# fields
    	dtCriterionComboBox = QComboBox(dtPage)
    	dtCriterionComboBox.addItem('gini')
    	dtCriterionComboBox.addItem('entropy')
    	dtMaxDepthLineEdit = QLineEdit('None', dtPage)
    	dtMinSamplesSplitSpinBox = self.__setSpinBox(2, 2, 20, 1, dtPage)
    	dtMinSamplesLeafSpinBox = self.__setSpinBox(1, 1, 20, 1, dtPage)
    	dtClassWeightLineEdit = QLineEdit('balanced', dtPage)

    	# layout
    	dtLayout = QFormLayout()
    	dtLayout.addRow('criterion:', dtCriterionComboBox)
    	dtLayout.addRow('max_depth:', dtMaxDepthLineEdit)
    	dtLayout.addRow('min_samples_split:', dtMinSamplesSplitSpinBox)
    	dtLayout.addRow('min_samples_leaf:', dtMinSamplesLeafSpinBox)
    	dtLayout.addRow('class_weight:', dtClassWeightLineEdit)

    	dtPageLayout = QVBoxLayout(dtPage)
    	dtPageLayout.addLayout(dtLayout)

    	## Random forest
    	rfIcon = QIcon('icons/rf.png')
    	classTypeComboBox.addItem(rfIcon, 'Random Forest')
    	rfPage = QWidget()
    	paramStack.addWidget(rfPage)

    	# fields
    	rfCriterionComboBox = QComboBox(rfPage)
    	rfCriterionComboBox.addItem('gini')
    	rfCriterionComboBox.addItem('entropy')
    	rfNumEstimatorsSpinBox = self.__setSpinBox(10, 1, 25, 1, rfPage)
    	rfMaxFeaturesComboBox = QComboBox(rfPage)
    	rfMaxFeaturesComboBox.addItem('sqrt')
    	rfMaxFeaturesComboBox.addItem('log2')
    	rfMaxFeaturesComboBox.addItem('None')
    	rfMaxDepthLineEdit = QLineEdit('None', rfPage)
    	rfMinSamplesSplitSpinBox = self.__setSpinBox(2, 2, 20, 1, rfPage)
    	rfMinSamplesLeafSpinBox = self.__setSpinBox(1, 1, 20, 1, rfPage)
    	rfBootstrapCheckBox = QCheckBox('', rfPage)
    	rfBootstrapCheckBox.setChecked(True)
    	rfClassWeightLineEdit = QLineEdit('balanced', rfPage)

    	# layout
    	rfLayout = QFormLayout()
    	rfLayout.addRow('criterion:', rfCriterionComboBox)
    	rfLayout.addRow('n_estimators:', rfNumEstimatorsSpinBox)
    	rfLayout.addRow('max_features:', rfMaxFeaturesComboBox)
    	rfLayout.addRow('max_depth:', rfMaxDepthLineEdit)
    	rfLayout.addRow('min_samples_split:', rfMinSamplesSplitSpinBox)
    	rfLayout.addRow('min_samples_leaf:', rfMinSamplesLeafSpinBox)
    	rfLayout.addRow('bootstrap:', rfBootstrapCheckBox)
    	rfLayout.addRow('class_weight:', rfClassWeightLineEdit)

    	rfPageLayout = QVBoxLayout(rfPage)
    	rfPageLayout.addLayout(rfLayout)

    	## K-nearest neighbors
    	knnIcon = QIcon('icons/knn.png')
    	classTypeComboBox.addItem(knnIcon, 'K-Nearest Neighbors')
    	knnPage = QWidget()
    	paramStack.addWidget(knnPage)

    	# fields
    	knnNumNeighborsSpinBox = self.__setSpinBox(5, 1, 20, 1, knnPage)
    	knnWeightsComboBox = QComboBox(knnPage)
    	knnWeightsComboBox.addItem('uniform')
    	knnWeightsComboBox.addItem('distance')
    	knnMetricLabel = QLabel('', knnPage)

    	# layout
    	knnLayout = QFormLayout()
    	knnLayout.addRow('n_neighbors:', knnNumNeighborsSpinBox)
    	knnLayout.addRow('weights:', knnWeightsComboBox)
    	knnLayout.addRow('metric:', knnMetricLabel)

    	knnPageLayout = QVBoxLayout(knnPage)
    	knnPageLayout.addLayout(knnLayout)

    	## Logistic regression
    	lrIcon = QIcon('icons/lr.png')
    	classTypeComboBox.addItem(lrIcon, 'Logistic Regression')
    	lrPage = QWidget()
    	paramStack.addWidget(lrPage)

    	# fields
    	lrRegularizationComboBox = QComboBox(lrPage)
    	lrRegularizationComboBox.addItem('l2')
    	lrRegularizationComboBox.addItem('l1')
    	lrRglrStrengthDoubleSpinBox = self.__setDoubleSpinBox(1, 0, 10, 0.1, 1, lrPage)
    	lrFitInterceptCheckBox = QCheckBox('', lrPage)
    	lrFitInterceptCheckBox.setChecked(True)
    	lrMultiClassComboBox = QComboBox(lrPage)
    	lrMultiClassComboBox.addItem('ovr')
    	lrMultiClassComboBox.addItem('multinomial')
    	lrClassWeightLineEdit = QLineEdit('balanced', lrPage)

    	lrStopLabel = QLabel('Stopping Criteria:', lrPage)
    	lrTolLabel = QLabel('tol:', lrPage)
    	lrTolLabel.setMinimumWidth(60)
    	lrTolLineEdit = QLineEdit('1e-3', lrPage)
    	lrMaxIterLabel = QLabel('max_iter:', lrPage)
    	lrMaxIterLabel.setMinimumWidth(60)
    	lrMaxIterLineEdit = QLineEdit('100', lrPage)

    	# layout
    	lrLayout = QFormLayout()
    	lrLayout.addRow('regularization:', lrRegularizationComboBox)
    	lrLayout.addRow('rglr_strength:', lrRglrStrengthDoubleSpinBox)
    	lrLayout.addRow('fit_intercept:', lrFitInterceptCheckBox)
    	lrLayout.addRow('multi_class:', lrMultiClassComboBox)
    	lrLayout.addRow('class_weight:', lrClassWeightLineEdit)

    	lrSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

    	lrStopLayout = QHBoxLayout()
    	lrStopLayout.addWidget(lrTolLabel)
    	lrStopLayout.addWidget(lrTolLineEdit)
    	lrStopLayout.addWidget(lrMaxIterLabel)
    	lrStopLayout.addWidget(lrMaxIterLineEdit)

    	lrPageLayout = QVBoxLayout(lrPage)
    	lrPageLayout.addLayout(lrLayout)
    	lrPageLayout.addItem(lrSpacer)
    	lrPageLayout.addWidget(lrStopLabel)
    	lrPageLayout.addLayout(lrStopLayout)

    	## Neural Network
    	nnIcon = QIcon('icons/nn.png')
    	classTypeComboBox.addItem(nnIcon, 'Neural Network')
    	nnPage = QWidget()
    	paramStack.addWidget(nnPage)

    	# fields
    	nnNumHiddenUnitsSpinBox = self.__setSpinBox(0, 0, 10, 1, nnPage)
    	nnActivationComboBox = QComboBox(nnPage)
    	nnActivationComboBox.addItem('relu')
    	nnActivationComboBox.addItem('logistic')
    	nnActivationComboBox.addItem('tanh')
    	nnActivationComboBox.addItem('identity')
    	nnBatchSizeLineEdit = QLineEdit('auto', nnPage)
    	nnLearningRateComboBox = QComboBox(nnPage)
    	nnLearningRateComboBox.addItem('constant')
    	nnLearningRateComboBox.addItem('invscaling')
    	nnLearningRateComboBox.addItem('adaptive')
    	nnLearningRateInitLineEdit = QLineEdit('0.001', nnPage)
    	nnEarlyStoppingCheckBox = QCheckBox('', nnPage)

    	nnStopLabel = QLabel('Stopping Criteria:', nnPage)
    	nnTolLabel = QLabel('tol:', nnPage)
    	nnTolLabel.setMinimumWidth(60)
    	nnTolLineEdit = QLineEdit('1e-3', nnPage)
    	nnMaxIterLabel = QLabel('max_iter:', nnPage)
    	nnMaxIterLabel.setMinimumWidth(60)
    	nnMaxIterLineEdit = QLineEdit('100', nnPage)

    	# layout
    	nnLayout = QFormLayout()
    	nnLayout.addRow('num_hidden_units:', nnNumHiddenUnitsSpinBox)
    	nnLayout.addRow('activation:', nnActivationComboBox)
    	nnLayout.addRow('batch_size:', nnBatchSizeLineEdit)
    	nnLayout.addRow('learning_rate:', nnLearningRateComboBox)
    	nnLayout.addRow('learning_rate_init:', nnLearningRateInitLineEdit)
    	nnLayout.addRow('early_stopping:', nnEarlyStoppingCheckBox)

    	nnSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

    	nnStopLayout = QHBoxLayout()
    	nnStopLayout.addWidget(nnTolLabel)
    	nnStopLayout.addWidget(nnTolLineEdit)
    	nnStopLayout.addWidget(nnMaxIterLabel)
    	nnStopLayout.addWidget(nnMaxIterLineEdit)

    	nnPageLayout = QVBoxLayout(nnPage)
    	nnPageLayout.addLayout(nnLayout)
    	nnPageLayout.addItem(nnSpacer)
    	nnPageLayout.addWidget(nnStopLabel)
    	nnPageLayout.addLayout(nnStopLayout)

    	## SVM
    	svmIcon = QIcon('icons/svm.png')
    	classTypeComboBox.addItem(svmIcon, 'SVM')
    	svmPage = QWidget()
    	paramStack.addWidget(svmPage)

    	# fields
    	svmPenaltyDoubleSpinBox = self.__setDoubleSpinBox(1, 0, 10, 0.1, 1, svmPage)
    	svmKernelComboBox = QComboBox(svmPage)
    	svmKernelComboBox.addItem('rbf')
    	svmKernelComboBox.addItem('linear')
    	svmKernelComboBox.addItem('polynomial')
    	svmKernelComboBox.addItem('sigmoid')
    	svmDegreeSpinBox = self.__setSpinBox(3, 1, 5, 1, svmPage)
    	svmGammaLineEdit = QLineEdit('auto')
    	svmCoefDoubleSpinBox = self.__setDoubleSpinBox(0, -10, 10, 0.1, 1, svmPage)
    	svmClassWeightLineEdit = QLineEdit('balanced')

    	svmStopLabel = QLabel('Stopping Criteria:', svmPage)
    	svmTolLabel = QLabel('tol:', svmPage)
    	svmTolLabel.setMinimumWidth(60)
    	svmTolLineEdit = QLineEdit('1e-3', svmPage)
    	svmMaxIterLabel = QLabel('max_iter:', svmPage)
    	svmMaxIterLabel.setMinimumWidth(60)
    	svmMaxIterLineEdit = QLineEdit('100', svmPage)

    	# layout
    	svmLayout = QFormLayout()
    	svmLayout.addRow('penalty:', svmPenaltyDoubleSpinBox)
    	svmLayout.addRow('kernel:', svmKernelComboBox)
    	svmLayout.addRow('degree:', svmDegreeSpinBox)
    	svmLayout.addRow('gamma:', svmGammaLineEdit)
    	svmLayout.addRow('coef0:', svmCoefDoubleSpinBox)
    	svmLayout.addRow('class_weight:', svmClassWeightLineEdit)

    	svmSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

    	svmStopLayout = QHBoxLayout()
    	svmStopLayout.addWidget(svmTolLabel)
    	svmStopLayout.addWidget(svmTolLineEdit)
    	svmStopLayout.addWidget(svmMaxIterLabel)
    	svmStopLayout.addWidget(svmMaxIterLineEdit)

    	svmPageLayout = QVBoxLayout(svmPage)
    	svmPageLayout.addLayout(svmLayout)
    	svmPageLayout.addItem(svmSpacer)
    	svmPageLayout.addWidget(svmStopLabel)
    	svmPageLayout.addLayout(svmStopLayout)

    	## Naive bayes
    	nbIcon = QIcon('icons/nb.png')
    	classTypeComboBox.addItem(nbIcon, 'Naive Bayes')
    	nbPage = QWidget()
    	paramStack.addWidget(nbPage)

    	# fields
    	nbDistributionLabel = QLabel('')
    	nbAddSmoothDoubleSpinBox = self.__setDoubleSpinBox(1, 0, 50, 0.5, 1, nbPage)
    	nbFitPriorCheckBox = QCheckBox(nbPage)
    	nbFitPriorCheckBox.setChecked(True)
    	nbClassPriorLineEdit = QLineEdit('None', nbPage)

    	nbStopLabel = QLabel('Stopping Criteria:', nbPage)
    	nbTolLabel = QLabel('tol:', nbPage)
    	nbTolLabel.setMinimumWidth(60)
    	nbTolLineEdit = QLineEdit('1e-3', nbPage)
    	nbMaxIterLabel = QLabel('max_iter:', nbPage)
    	nbMaxIterLabel.setMinimumWidth(60)
    	nbMaxIterLineEdit = QLineEdit('100', nbPage)

    	# layout
    	nbLayout = QFormLayout()
    	nbLayout.addRow('distributon:', nbDistributionLabel)
    	nbLayout.addRow('add_smooth:', nbAddSmoothDoubleSpinBox)
    	nbLayout.addRow('fit_prior:', nbFitPriorCheckBox)
    	nbLayout.addRow('class_prior:', nbClassPriorLineEdit)

    	nbSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

    	nbStopLayout = QHBoxLayout()
    	nbStopLayout.addWidget(nbTolLabel)
    	nbStopLayout.addWidget(nbTolLineEdit)
    	nbStopLayout.addWidget(nbMaxIterLabel)
    	nbStopLayout.addWidget(nbMaxIterLineEdit)

    	nbPageLayout = QVBoxLayout(nbPage)
    	nbPageLayout.addLayout(nbLayout)
    	nbPageLayout.addItem(nbSpacer)
    	nbPageLayout.addWidget(nbStopLabel)
    	nbPageLayout.addLayout(nbStopLayout)

    	### classifier name
    	classNameLabel = self.__setLabel('Classifier Name:', modelPage, titleFont)
    	classNameLineEdit = QLineEdit(modelPage)
    	classNameLineEdit.setDisabled(True)
    	paramStack.currentChanged.connect(lambda: classNameLineEdit.setEnabled(paramStack.currentIndex() > 0))

    	classNameLayout = QHBoxLayout()
    	classNameLayout.addWidget(classNameLabel)
    	classNameLayout.addWidget(classNameLineEdit)

    	modelPageLayout.addLayout(classNameLayout)

    	### comment
    	classCommentLabel = self.__setLabel('Comment:', modelPage, titleFont)
    	classCommentTextEdit = QTextEdit(modelPage)
    	classCommentTextEdit.setMaximumHeight(50)
    	classCommentTextEdit.setDisabled(True)
    	paramStack.currentChanged.connect(lambda: classCommentTextEdit.setEnabled(paramStack.currentIndex() > 0))

    	modelPageLayout.addWidget(classCommentLabel)
    	modelPageLayout.addWidget(classCommentTextEdit)

    	### reset and train buttons
    	classResetTrainSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    	classResetPushButton = QPushButton('Reset', modelPage)
    	classResetPushButton.setMinimumWidth(90)
    	classResetPushButton.setDisabled(True)
    	paramStack.currentChanged.connect(lambda: classResetPushButton.setEnabled(paramStack.currentIndex() > 0))
    	classTrainPushButton = QPushButton('Train', modelPage)
    	classTrainPushButton.setMinimumWidth(90)
    	classTrainPushButton.setDefault(True)
    	classTrainPushButton.setDisabled(True)
    	paramStack.currentChanged.connect(lambda: classTrainPushButton.setEnabled(paramStack.currentIndex() > 0))

    	classResetTrainLayout = QHBoxLayout()
    	classResetTrainLayout.addItem(classResetTrainSpacer)
    	classResetTrainLayout.addWidget(classResetPushButton)
    	classResetTrainLayout.addWidget(classTrainPushButton)

    	modelPageLayout.addLayout(classResetTrainLayout)

    	### page spacer and line
    	modelPageSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
    	modelPageLayout.addItem(modelPageSpacer)
    	modelLine = QFrame(modelPage)
    	modelLine.setFrameShape(QFrame.HLine)
    	modelLine.setFrameShadow(QFrame.Sunken)
    	modelPageLayout.addWidget(modelLine)

    	### back and next buttons
    	classBackNextSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    	classBackPushButton = QPushButton('Back', modelPage)
    	classBackPushButton.setMinimumWidth(90)
    	classBackPushButton.clicked.connect(lambda: self.leftPanel.setCurrentIndex(0))
    	classNextPushButton = QPushButton('Next', modelPage)
    	classNextPushButton.setMinimumWidth(90)
    	classNextPushButton.setDefault(True)
    	classNextPushButton.setDisabled(True)
    	classTrainPushButton.clicked.connect(lambda: classNextPushButton.setEnabled(True))
    	classNextPushButton.clicked.connect(lambda: self.leftPanel.setCurrentIndex(2))

    	classBackNextLayout = QHBoxLayout()
    	classBackNextLayout.addItem(classBackNextSpacer)
    	classBackNextLayout.addWidget(classBackPushButton)
    	classBackNextLayout.addWidget(classNextPushButton)

    	modelPageLayout.addLayout(classBackNextLayout)

    	self.leftPanel.addWidget(modelPage)


    	########## 3rd page: model selection and testing ##########
    	testPage = QWidget()
    	testPageLayout = QVBoxLayout(testPage)

    	### classifier selection
    	classSelectLabel = self.__setLabel('Classifier Selection:', testPage, titleFont)
    	testPageLayout.addWidget(classSelectLabel)

    	classSelectFrame = QFrame(testPage)
    	classSelectFrame.setAutoFillBackground(True)
    	classSelectLayout = QVBoxLayout(classSelectFrame)
    	bestPerformRadioButton = QRadioButton('Best-Performing', classSelectFrame)
    	bestPerformRadioButton.setChecked(True)
    	userPickRadioButton = QRadioButton('User-Picked', classSelectFrame)
    	bestPerformSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    	metricLabel = QLabel('Metric', classSelectFrame)
    	metricComboBox = QComboBox(classSelectFrame)
    	metricComboBox.addItem('accuracy')
    	metricComboBox.addItem('recall')
    	metricComboBox.addItem('specificity')
    	metricComboBox.addItem('precision')
    	metricComboBox.addItem('F1')
    	metricComboBox.addItem('AUROC')
    	metricComboBox.addItem('AUPRC')
    	bestPerformRadioButton.toggled.connect(metricComboBox.setEnabled)
    	userPickRadioButton.toggled.connect(metricComboBox.setDisabled)
    	userPickLabel = QLabel('<classifierName>', classSelectFrame)
    	userPickLabel.setMinimumWidth(150)
    	
    	bestPerformLayout = QHBoxLayout()
    	bestPerformLayout.addWidget(bestPerformRadioButton)
    	bestPerformLayout.addItem(bestPerformSpacer)
    	bestPerformLayout.addWidget(metricLabel)
    	bestPerformLayout.addWidget(metricComboBox)
    	classSelectLayout.addLayout(bestPerformLayout)

    	userPickLayout = QHBoxLayout()
    	userPickLayout.addWidget(userPickRadioButton)
    	userPickLayout.addWidget(userPickLabel)
    	classSelectLayout.addLayout(userPickLayout)

    	testPageLayout.addWidget(classSelectFrame)

    	### test button
    	testPushButton = QPushButton('Test')
    	testPushButton.setMinimumWidth(90)
    	testPushButton.setDefault(True)
    	testSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    	testLayout = QHBoxLayout()
    	testLayout.addItem(testSpacer)
    	testLayout.addWidget(testPushButton)
    	testPageLayout.addLayout(testLayout)

    	### test result
    	testResultLabel = self.__setLabel('Test Result:', testPage, titleFont)
    	testResultList = QListView(testPage)
    	testResultList.setMinimumHeight(250)
    	testPageLayout.addWidget(testResultLabel)
    	testPageLayout.addWidget(testResultList)

    	### prediction button
    	predictionLabel = self.__setLabel('Prediction:', testPage, titleFont)
    	self.predictionPushButton = QPushButton('Predict and Save As...', testPage)
    	self.predictionPushButton.setMaximumWidth(175)
    	self.predictionPushButton.setDisabled(True)
    	predictionLayout = QHBoxLayout()
    	predictionLayout.addWidget(predictionLabel)
    	predictionLayout.addWidget(self.predictionPushButton)
    	testPageLayout.addLayout(predictionLayout)

    	### page spacer and line
    	testPageSpacer = QSpacerItem(40, 20,QSizePolicy.Minimum, QSizePolicy.Expanding)
    	testPageLayout.addItem(testPageSpacer)
    	testLine = QFrame(testPage)
    	testLine.setFrameShape(QFrame.HLine)
    	testLine.setFrameShadow(QFrame.Sunken)
    	testPageLayout.addWidget(testLine)

    	### back and finish buttons
    	testBackPushButton = QPushButton('Back', testPage)
    	testBackPushButton.setMinimumWidth(90)
    	testBackPushButton.clicked.connect(lambda: self.leftPanel.setCurrentIndex(1))
    	testPushButton.clicked.connect(lambda: testBackPushButton.setDisabled(True))
    	testFinishPushButton = QPushButton('Finish', testPage)
    	testFinishPushButton.setMinimumWidth(90)
    	testFinishPushButton.setDefault(True)
    	testFinishPushButton.setDisabled(True)
    	testPushButton.clicked.connect(lambda: testFinishPushButton.setEnabled(True))
    	testBackFinishSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    	testBackFinishLayout = QHBoxLayout()
    	testBackFinishLayout.addItem(testBackFinishSpacer)
    	testBackFinishLayout.addWidget(testBackPushButton)
    	testBackFinishLayout.addWidget(testFinishPushButton)
    	testPageLayout.addLayout(testBackFinishLayout)

    	self.leftPanel.addWidget(testPage)


    	########## right panel ##########
    	rightPanelLayout = QVBoxLayout(self.rightPanel)

    	### trained classifiers
    	trainedClassifiersLabel = self.__setLabel('Trained Classifiers:', self.rightPanel, titleFont)
    	trainedClassifiersList = QListView(self.rightPanel)
    	rightPanelLayout.addWidget(trainedClassifiersLabel)
    	rightPanelLayout.addWidget(trainedClassifiersList)

    	### visualization panel
    	visLayout = QHBoxLayout()
    	visListLayout = QVBoxLayout()
    	visList = QListView(self.rightPanel)
    	visList.setMaximumWidth(245)
    	visListLayout.addWidget(visList)

    	visFrame = QFrame(self.rightPanel)
    	visFrameLayout = QVBoxLayout(visFrame)
    	dataPlotRadioButton = QRadioButton('Data Plot', visFrame)
    	rocRadioButton = QRadioButton('ROC', visFrame)
    	confusionMatrixRadioButton = QRadioButton('Confusion Matrix', visFrame)
    	prRadioButton = QRadioButton('Precision-Recall', visFrame)
    	visFrameLeftLayout = QVBoxLayout()
    	visFrameLeftLayout.addWidget(dataPlotRadioButton)
    	visFrameLeftLayout.addWidget(rocRadioButton)
    	visFrameRightLayout = QVBoxLayout()
    	visFrameRightLayout.addWidget(confusionMatrixRadioButton)
    	visFrameRightLayout.addWidget(prRadioButton)
    	visFrameTopLayout = QHBoxLayout()
    	visFrameTopLayout.addLayout(visFrameLeftLayout)
    	visFrameTopLayout.addLayout(visFrameRightLayout)

    	visFrameSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    	visSavePushButton = QPushButton('Save As...', visFrame)
    	saveIcon = QIcon('icons/save.png')
    	visSavePushButton.setIcon(saveIcon)
    	visFrameBottomLayout = QHBoxLayout()
    	visFrameBottomLayout.addItem(visFrameSpacer)
    	visFrameBottomLayout.addWidget(visSavePushButton)
    	visFrameLayout.addLayout(visFrameTopLayout)
    	visFrameLayout.addLayout(visFrameBottomLayout)
    	visListLayout.addWidget(visFrame)
    	visLayout.addLayout(visListLayout)

    	plotArea = QWidget(self.rightPanel)
    	plotArea.setFixedSize(340, 340)
    	plotArea.setAutoFillBackground(True)
    	visLayout.addWidget(plotArea)

    	rightPanelLayout.addLayout(visLayout)

    	self.resize(1024, 700)
    	self.setWindowTitle('ML4Bio')
    	self.leftPanel.resize(360, 680)
    	self.leftPanel.setStyleSheet("QStackedWidget {background-color:rgb(226, 226, 226)}")
    	self.leftPanel.move(10, 10)
    	self.rightPanel.resize(640, 680)
    	self.rightPanel.move(380, 10)

    	self.show()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())