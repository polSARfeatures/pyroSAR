import os
import sys
import pytest
import pyroSAR


def test_scene_osv(tmpdir, testdata):
    id = pyroSAR.identify(testdata['s1'])
    osvdir = os.path.join(str(tmpdir), 'osv')
    if sys.version_info >= (2, 7, 9):
        id.getOSV(osvdir)
        with pyroSAR.OSV(osvdir) as osv:
            with pytest.raises(IOError):
                osv.catch(osvtype='XYZ')
            res = osv.catch(osvtype='RES', start=osv.mindate('POE'), stop=osv.maxdate('POE'))
            assert len(res) == 21
            osv.retrieve(res[0:3])

            assert len(osv.getLocals('POE')) == 3
            assert len(osv.getLocals('RES')) == 3
            assert osv.match(id.start, 'POE') is not None
            assert osv.match(id.start, ['POE', 'RES']) is not None
            assert osv.match(id.start, 'RES') is None
            for item in osv.getLocals('POE')[1:3]:
                os.remove(item)
            assert len(osv.getLocals('POE')) == 1
            osv.clean_res()
    else:
        with pytest.raises(RuntimeError):
            id.getOSV(osvdir, osvType='POE')
