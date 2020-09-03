import functools
import os
import re
from textwrap import dedent

from domdf_python_tools.paths import PathPlus

from dotnet_stub_builder.utils import tab_in
from dotnet_stub_builder.type_conversion import Converter
from dotnet_stub_builder.makers import make_module, make_package

import sys
import platform

if platform.architecture()[0] == "64bit":
	sys.path.append(os.path.abspath("../pyms-agilent/pyms_agilent/mhdac/x64"))
else:
	sys.path.append(os.path.abspath("../pyms-agilent/pyms_agilent/mhdac/x86"))

import clr

clr.AddReference("MassSpecDataReader")
clr.AddReference("BaseCommon")
clr.AddReference("BaseDataAccess")

import Agilent
import Agilent.MassSpectrometry


class AgilentConverter(Converter):
	def __init__(self):
		super().__init__({
				"Agilent.MassSpectrometry.WtcCalibration": "Any",
				})

	def convert_type(self, csharp_type: str) -> str:
		csharp_type = re.sub(" ByRef$", '', csharp_type)

		if csharp_type in self.type_mapping:
			return self.type_mapping[csharp_type]

		elif re.match(r"^Agilent\.MassSpectrometry\.DataAnalysis\.([A-Za-z_]+)$", csharp_type):
			return re.match(r"^Agilent\.MassSpectrometry\.DataAnalysis\.([A-Za-z_]+)$", csharp_type).group(1)

		elif re.match(r"^Agilent\.MassSpectrometry\.DataAnalysis\.([A-Za-z_]+)\[]$", csharp_type):
			csharp_type = re.match(r"^Agilent\.MassSpectrometry\.DataAnalysis\.([A-Za-z_]+)\[]$", csharp_type).group(1)
			return f"List[{csharp_type}]"

		elif re.match(r"^Agilent\.MassSpectrometry\.[A-Za-z_]+$", csharp_type):
			return csharp_type

		else:
			return super().convert_type(csharp_type)


make_package = functools.partial(make_package, converter=AgilentConverter())
make_module = functools.partial(make_module, converter=AgilentConverter())


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
			[
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
					"IBDAActualData",
					"IBDAMSScanTypeInformation",
					"ICoreList",
					"BDAProgressEventArgs",
					"IBDASampleData",
					"IMSScanRecord",
					"ChangeNotifyDelegate",
					"IMsdrPeakFilter",
					"IMsdrChargeStateAssignmentFilter",
					],
			[
					"from pyms_agilent.enums import (",
					tab_in(dedent("""\
					DeviceType,
					StoredDataType,
					DataUnit,
					DataValueType,
					ChromType,
					ChromSubType,
					MSLevel,
					MSScanType,
					MSStorageMode,
					SpecType,
					SpecSubType,
					SampleCategory,
					IonizationMode,
					TofMsProcessingMode,
					)"""))
					])


if __name__ == '__main__':
	build_stubs()
	print("Done!")
