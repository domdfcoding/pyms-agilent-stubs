# stdlib
import functools
import os
import platform
import re
import sys

# 3rd party
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.stringlist import StringList
from dotnet_stub_builder.makers import make_module, make_package
from dotnet_stub_builder.type_conversion import Converter

if platform.architecture()[0] == "64bit":
	sys.path.append(os.path.abspath("../pyms-agilent/pyms_agilent/mhdac/x64"))
else:
	sys.path.append(os.path.abspath("../pyms-agilent/pyms_agilent/mhdac/x86"))

# 3rd party
import clr

clr.AddReference("MassSpecDataReader")
clr.AddReference("BaseCommon")
clr.AddReference("BaseDataAccess")

# this package
import Agilent
import Agilent.MassSpectrometry


class AgilentConverter(Converter):

	def __init__(self):
		super().__init__({
				"Agilent.MassSpectrometry.WtcCalibration":
						"Any",
				"Agilent.MassSpectrometry.MIDAC.FragmentationOpMode":
						"Any",
				"Agilent.MassSpectrometry.MIDAC.FragmentationClass":
						"Any",
				"System.Collections.Generic.Dictionary":
						"Dict",
				"SortDirection":
						"Any",
				"KeyCollection":
						"Any",
				"ValueCollection":
						"Any",
				"IonPolarity":
						"Any",
				"SmoothingFunctionType":
						"Any",
				"System.Collections.Generic.List`1[System.Int16]":
						"List[int]",
				"System.Collections.Generic.IEnumerable`1[System.Collections.Generic.KeyValuePair`2[System.Int32,"
				"Agilent.MassSpectrometry.DataAnalysis.IBdaMsScanRecInfo]]":
						"Any",
				})

	def convert_type(self, csharp_type: str) -> str:
		csharp_type = re.sub(" ByRef$", '', csharp_type)

		if csharp_type in self.type_mapping:
			return self.type_mapping[csharp_type]

		elif re.match(r"^Agilent\.MassSpectrometry\.DataAnalysis\.([A-Za-z_]+)$", csharp_type):
			return re.match(r"^Agilent\.MassSpectrometry\.DataAnalysis\.([A-Za-z_]+)$", csharp_type).group(1)

		elif re.match(r"^Agilent\.MassSpectrometry\.DataAnalysis\.([A-Za-z_]+)\[]$", csharp_type):
			csharp_type = re.match(r"^Agilent\.MassSpectrometry\.DataAnalysis\.([A-Za-z_]+)\[]$",
									csharp_type).group(1)
			return f"List[{csharp_type}]"

		elif re.match(r"^Agilent\.MassSpectrometry\.[A-Za-z_]+$", csharp_type):
			return csharp_type

		else:
			return super().convert_type(csharp_type)


make_package = functools.partial(make_package, converter=AgilentConverter())
make_module = functools.partial(make_module, converter=AgilentConverter())

attr_list = [
		"BDAFileInformation",
		"IBDAFileInformation",
		"IBDAChromData",
		"SignalInfo",
		"BDAChromData",
		"MSOverallScanRecordInfo",
		"BDARangeCollection",
		"MassSpecDataReader",
		"IMsdrDataReader",
		"MsdrPeakFilter",
		"DeviceInfo",
		"IBDAActuals",
		"IBDAChromFilter",
		"BDAChromFilter",
		"IBDASpecData",
		"BDADataAccess",
		"BDAMSScanFileInformation",
		"IBDAMSScanFileInformation",
		"ISignalInfo",
		"BDASpecData",
		"IBDAMsDeviceInfo",
		"BDAProgressEventHandler",
		"IRange",
		"IDeviceInfo",
		"DisposableBase",
		"XSamplingType",
		"IUnitsAndPrecision",
		"IReadOnlyObject",
		"DisplayPrecisionType",
		"IBDAActualData",
		"IBDASpecFilter",
		"BDAMSScanTypeInformation",
		"IBDAMSScanTypeInformation",
		"ICoreList",
		"BDAProgressEventArgs",
		"BDASampleData",
		"IBDASampleData",
		"MSScanRecord",
		"IMSScanRecord",
		"ChangeNotifyDelegate",
		"IMsdrPeakFilter",
		"IMsdrChargeStateAssignmentFilter",
		"CenterWidthPctRange",
		"MinMaxRange",
		"IMinMaxRange",
		"ICenterWidthPctRange",
		"RangeBase",
		"CenterWidthRange",
		"ICenterWidthRange",
		"AsymmetricRange",
		"IAsymmetricRange",
		"CenterWidthPpmRange",
		"ICenterWidthPpmRange",
		"INonmsDataReader",
		"IBDASample",
		"IImsFrameMethod",
		"IBDAUserCalibration",
		"IBDADataAccess",
		"BDAAcquisitionData",
		"IBDAAcquisitionData",
		"IBDAEvents",
		"BDASpecFilterIcp",
		"IBDASpecFilterIcp",
		"BDAChromFilterIcp",
		"IBDAChromFilterIcp",
		"IBDAReadChromatogram",
		"IBDAReadSpectra",
		"BDAPeakSpecFilter",
		"IBDAPeakSpecFilter",
		"IBDAPeak",
		"IBdaMsScanRecordCollection",
		"IBDAMultiEicParameters",
		"IBDAPeakSpectrumParameters",
		"IBDASpecPair",
		"ILwChromPeak",
		"BDAPeak",
		"IImsFrameRecord",
		"ImsFrameScanRec",
		"BDASpecFilter",
		"ImsFrameMethod",
		"PointValueFormat",
		"BDAActualData",
		"MsdrChargeStateAssignmentFilter",
		"IFragEnergySegmentEndPoint",
		"IBdaMsScanRecInfo",
		"IEicRtMzRanges",
		"LwPeakAttribute",
		"LwPeakEndFlags",
		"LwPeakWarning",
		"IImsScanRecord",
		"IMsSpecAccessParams",
		"IMsSpectrumFmt",
		"IMsValueFmt",
		]

extra_imports = StringList([
		'', "from typing import Optional, overload, Tuple, Union", '', "from pyms_agilent.enums import ("
		])

with extra_imports.with_indent("    ", 2):
	extra_imports.extend([
			"DeviceType,",
			"StoredDataType,",
			"DataUnit,",
			"DataValueType,",
			"ChromType,",
			"ChromSubType,",
			"MSLevel,",
			"MSScanType,",
			"MSStorageMode,",
			"SpecType,",
			"SpecSubType,",
			"SampleCategory,",
			"IonizationMode,",
			"TofMsProcessingMode,",
			"DataFileValueDataType,",
			"PointValueStorageScheme,",
			"ImsFrameType,",
			"DesiredMSStorageType,",
			"ApseBackgroundSource,",
			"IonDetectorGain,",
			"FragmentationOpMode,",
			"FragmentationClass,",
			')',
			])

extra_imports.blankline(ensure_single=True)
extra_imports.extend(["IonPolarity = int", "SmoothingFunctionType = Any"])
extra_imports.blankline(ensure_single=True)


def build_stubs():
	stubs_dir = PathPlus("Agilent-stubs")
	(stubs_dir / "__init__.pyi").touch(exist_ok=True)
	(stubs_dir / "MassSpectrometry").maybe_make(parents=True)
	(stubs_dir / "MassSpectrometry" / "__init__.pyi").touch(exist_ok=True)

	make_package("Agilent", Agilent, [])
	make_package("Agilent.MassSpectrometry", Agilent.MassSpectrometry, [])

	make_module(
			"Agilent.MassSpectrometry.DataAnalysis",
			Agilent.MassSpectrometry.DataAnalysis,
			attr_list,
			list(extra_imports)
			)


if __name__ == "__main__":
	build_stubs()
	print("Done!")
