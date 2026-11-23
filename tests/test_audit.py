import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from bic_validation_claim_audit.audit import audit, claims, evidence
from bic_validation_claim_audit.phrases import BICVALIDATION, NOBICVALIDATION, GENERIC_NAMES

ROOT = Path(__file__).resolve().parents[1]

class AuditTests(unittest.TestCase):
    def test_routes(self):
        routes = ["import schwifty\nschwifty.BIC(x)", "import schwifty.bic\nschwifty.bic.BIC(x)", "import schwifty.bic as s\ns.BIC(x)", "from schwifty import BIC as b\nb(x)", "from schwifty.bic import BIC\nBIC(x)", "from schwifty import BIC\nBIC(x, True).validate()", "from schwifty import BIC\nBIC(x, True).is_valid", "from schwifty import BIC\nb = BIC(x, True)\nb.is_valid", "from schwifty import BIC\nwith BIC(x, True) as b: b.validate()"]
        for module in ('bic', 'iso9362'):
            for name in ('validate', 'is_valid'):
                routes.extend(['import stdnum\nstdnum.%s.%s(x)' % (module,name), 'import stdnum.%s\nstdnum.%s.%s(x)' % (module,module,name), 'from stdnum import %s as b\nb.%s(x)' % (module,name), 'from stdnum.%s import %s as f\nf(x)' % (module,name)])
        routes += ['obj.%s(x)' % n for n in GENERIC_NAMES]
        routes += ['from library import %s as f\nf(x)' % n for n in GENERIC_NAMES]
        routes += ['obj = make()\nobj.validate_bic(x)']
        for route in routes:
            with self.subTest(route=route): self.assertTrue(evidence(route))

    def test_not_evidence(self):
        cases = ['import schwifty', 'import stdnum.bic', 'BIC(x)', 'validate(x)', 'is_valid(x)', 'x.BIC(x)', 'x.validate(x)', 'x.is_valid', 'from schwifty import BIC\nBIC(x, allow_invalid=True)', 'from schwifty import BIC\nBIC(x, True)', 'from schwifty import BIC\nBIC.from_bank_code(x)', 'from schwifty import BIC\nBIC.candidates_from_bank_code(x)', 'import schwifty\nschwifty.IBAN(x)', 'import schwifty\nschwifty.BBAN(x)', 'import stdnum\nstdnum.iban.validate(x)', 'import stdnum\nstdnum.iban.is_valid(x)', 'import re\nre.match("pattern",x)', 'import re\nre.search("pattern",x)', 'import re\nre.fullmatch("pattern",x)', 'import pycountry\npycountry.countries.get(alpha_2=x)', 'from urllib.parse import urlparse\nurlparse(x)', 'from urllib.parse import urlsplit\nurlsplit(x)', 'import netaddr\nnetaddr.IPAddress(x)', 'import netaddr\nnetaddr.EUI(x)', 'import isbnlib\nisbnlib.is_isbn10(x)', 'import packaging.version\npackaging.version.Version(x)', 'import semver\nsemver.Version.parse(x)', 'payments.charge(x)', 'extractor.extract(x)', 'import subprocess\nsubprocess.run(["validate_bic"])', '"validate bic"', '# validate_bic(x)', 'from schwifty import BIC\ndef BIC(x): pass\nBIC(x)', 'import schwifty\nschwifty = 3\nschwifty.BIC(x)', 'from lib import validate_bic\nwith x as validate_bic: pass\nvalidate_bic(x)', 'validate_bic(x)', 'x.validate_bic(']
        cases += ['import validators\nvalidators.%s(x)' % n for n in ('url','ipv4','ipv6','email','card_number','domain','uuid','mac_address')]
        cases += ['from schwifty import BIC\nBIC.%s' % n for n in ('bank_code','country_code','location_code','branch_code','formatted','compact','length','banks','bank','bank_name','bank_short_name','bank_short_names','bank_names','country','type','exists','sepa_schemes','domestic_bank_codes','country_bank_code','canonical')]
        cases += ['import stdnum\nstdnum.bic.%s(x)' % n for n in ('compact','format')]
        for case in cases:
            with self.subTest(case=case): self.assertFalse(evidence(case))

    def test_phrases(self):
        self.assertEqual((len(BICVALIDATION),len(NOBICVALIDATION),len(GENERIC_NAMES)),(50,24,24))
        for phrase in BICVALIDATION:
            with self.subTest(phrase=phrase): self.assertTrue(claims(phrase)[0])
        for phrase in NOBICVALIDATION:
            with self.subTest(phrase=phrase): self.assertTrue(claims(phrase)[1]); self.assertFalse(claims(phrase)[0])
        self.assertEqual(claims('```\nvalidate bic\n```'),(set(),set()))
        self.assertTrue(claims('`validate bic`')[0])

    def test_findings(self):
        with TemporaryDirectory() as d:
            p=Path(d); (p/'README.md').write_text('validate bic')
            self.assertEqual(audit(p)[0]['severity'],'HIGH')
            (p/'tests').mkdir(); (p/'tests/test_x.py').write_text('import schwifty\nschwifty.BIC(x)')
            self.assertEqual(audit(p)[0]['severity'],'MEDIUM')
            (p/'x.py').write_text('import schwifty\nschwifty.BIC(x)')
            self.assertEqual(audit(p),[])
            (p/'README.md').write_text('no bic validation')
            self.assertEqual(audit(p)[0]['severity'],'HIGH')
            self.assertEqual(audit(p,['x.py']),[])
            (p/'README.md').write_text('validate bic'); (p/'x.py').write_text('import schwifty'); (p/'y.py').write_text('schwifty.BIC(x)')
            self.assertEqual(audit(p)[0]['severity'],'MEDIUM')

    def test_self_audit(self):
        self.assertEqual(audit(ROOT),[])
        self.assertEqual(audit(ROOT/'README.md'),[])

    def test_readme_limitations_prose(self):
        self.assertEqual(claims((ROOT/'README.md').read_text().split('## Limitations',1)[1]),(set(),set()))
