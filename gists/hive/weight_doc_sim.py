#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2023-02-22 19:34
Author:
    imhuay (imhuay@163.com)
Subject:
    doc_sim_weighted
References:
    <<A Framework for Robust Discovery of Entity Synonyms>>
"""
from __future__ import annotations

# import os
# import unittest
import sys
import platform
import json
import logging
import argparse
# import math

from typing import *

# from pathlib import Path
# from collections import defaultdict


test_data = [
    # 'a\te\t{"a":1,"b":20,"c":30}\t{"a":10,"c":20,"d":5}\t1\n',
    # 'a b\tf\t{"a":1,"b":20,"c":30}\t{"a":10,"c":20,"d":5}\t2\t3\n',
    'medical kit\tfirst aid kit\t1\t{"kit":133,"first":117,"aid":106,"emergency":50,"camping":42,"car":38,"medical":38,"trauma":38,"survival":35,"home":33,"hiking":30,"travel":28,"bag":25,"piece":24,"outdoor":21,"emt":20,"ifak":20,"tactical":18,"molle":16,"supplies":16,"office":15,"kits":14,"pouch":14,"responder":13,"stocked":13,"x":13,"bleeding":12,"hunting":12,"pcs":12,"military":11,"pieces":11,"gear":10,"control":9,"lightning":9,"rescue":9,"sports":9,"tourniquet":9,"adventure":8,"bandage":8,"premium":8,"school":8,"device":7,"ems":7,"fill":7,"portable":7,"system":7,"waterproof":7,"chest":6,"combat":6,"everlit":6,"seal":6,"boat":5,"care":5,"case":5,"compact":5,"equipment":5,"israeli":5,"medic":5,"osha":5,"practice":5,"purpose":5,"w":5,"wounds":5,"advanced":4,"backpack":4,"choking":4,"complete":4,"dad":4,"earthquake":4,"emergencies":4,"essentials":4,"fully":4,"gauze":4,"gen":4,"husband":4,"ideal":4,"johnson":4,"med":4,"pc":4,"people":4,"preparedness":4,"response":4,"rhino":4,"scherber":4,"scissors":4,"splint":4,"suture":4,"tool":4,"vent":4,"workplace":4,"wound":4,"adventures":3,"asa":3,"backpacking":3,"blanket":3,"clean":3,"compartments":3,"compatible":3,"cpr":3,"hard":3,"hyfin":3,"m":3,"mil":3,"mountain":3,"nylon":3,"outdoors":3,"pad":3,"pads":3,"perfect":3,"protect":3,"ready":3,"series":3,"set":3,"spec":3,"survivd":3,"techmed":3,"vehicle":3,"yiderbo":3,"accessories":2,"adult":2,"amk":2,"ansi":2,"bandages":2,"basics":2,"bladder":2,"bleed":2,"blood":2,"boating":2,"bonus":2,"breakwater":2,"business":2,"businesses":2,"cars":2,"compliant":2,"comprehensive":2,"count":2,"cut":2,"d":2,"dressing":2,"essential":2,"exceeds":2,"family":2,"foil":2,"get":2,"gift":2,"gifts":2,"gloves":2,"guidelines":2,"gunshot":2,"hydration":2,"ice":2,"includes":2,"including":2,"injuries":2,"items":2,"kids":2,"laser":2,"minor":2,"mountable":2,"multi":2,"multicam":2,"normatec":2,"pack":2,"person":2,"plastic":2,"powder":2,"prepared":2,"safe":2,"safety":2,"severe":2,"shears":2,"skin":2,"smart":2,"sof":2,"sterile":2,"students":2,"style":2,"surviveware":2,"swiss":2,"tourniquets":2,"traveling":2,"treat":2,"ultralight":2,"upgrade":2,"upgraded":2,"vented":2,"wall":2,"watertight":2,"work":2,"accident":1,"adhesive":1,"adjustable":1,"adults":1,"alcohol":1,"american":1,"amorning":1,"approved":1,"assorted":1,"away":1,"b":1,"basic":1,"battle":1,"belt":1,"biking":1,"birthday":1,"bleedstop":1,"bottle":1,"box":1,"boyfriend":1,"breathing":1,"bug":1,"buried":1,"cabinet":1,"camo":1,"camp":1,"camper":1,"carlebben":1,"carry":1,"christmas":1,"cleared":1,"close":1,"closure":1,"clotting":1,"clozex":1,"cold":1,"college":1,"combine":1,"combo":1,"comes":1,"compression":1,"constipation":1,"contol":1,"contractor":1,"cover":1,"coyote":1,"cuts":1,"cycling":1,"day":1,"deftget":1,"demo":1,"desert":1,"designed":1,"developed":1,"diaper":1,"disaster":1,"disasters":1,"doctor":1,"dorm":1,"dose":1,"doses":1,"dual":1,"durable":1,"dynamic":1,"dynarex":1,"edc":1,"edu":1,"education":1,"eva":1,"evantek":1,"ever":1,"everone":1,"everyday":1,"explorer":1,"eyewash":1,"fae":1,"falcontac":1,"fao":1,"father":1,"fda":1,"field":1,"fishing":1,"forceps":1,"fsa":1,"g":1,"gczlsc":1,"generation":1,"gentle":1,"genuine":1,"go":1,"going":1,"goods":1,"grade":1,"guide":1,"gun":1,"handed":1,"hardcase":1,"hatchet":1,"hemorrhage":1,"hemostat":1,"hiker":1,"hsa":1,"hyperice":1,"incision":1,"individual":1,"infant":1,"instruments":1,"iv":1,"jumbo":1,"keep":1,"kitchen":1,"knot":1,"labeled":1,"labelled":1,"laceration":1,"lantern":1,"latest":1,"latex":1,"laxative":1,"layer":1,"legs":1,"length":1,"life":1,"light":1,"lightweight":1,"loved":1,"made":1,"mask":1,"masks":1,"massage":1,"mb":1,"medications":1,"medkit":1,"miralax":1,"mixing":1,"model":1,"moderate":1,"modular":1,"moleskin":1,"motorcycle":1,"needles":1,"nosebleeds":1,"nurses":1,"nursing":1,"o":1,"od":1,"ones":1,"organized":1,"oxygen":1,"packed":1,"pair":1,"patented":1,"patients":1,"personal":1,"phlebotomy":1,"pliers":1,"pockets":1,"police":1,"pouches":1,"prep":1,"professionals":1,"pupil":1,"purse":1,"pysanr":1,"quality":1,"quikclot":1,"real":1,"recovery":1,"refill":1,"reflective":1,"relief":1,"removable":1,"removal":1,"repair":1,"resistant":1,"respirator":1,"rip":1,"saving":1,"science":1,"scrapes":1,"self":1,"shell":1,"shots":1,"shoulder":1,"shovel":1,"simulated":1,"sized":1,"skills":1,"smartcompliance":1,"sos":1,"st":1,"standard":1,"stealth":1,"stirrers":1,"stitches":1,"stop":1,"strap":1,"student":1,"suction":1,"suitcase":1,"surplus":1,"tape":1,"technology":1,"tent":1,"thinner":1,"thread":1,"threads":1,"thriaid":1,"thrive":1,"top":1,"touroam":1,"training":1,"trip":1,"truck":1,"trucks":1,"tsa":1,"u":1,"ultrassist":1,"unique":1,"urgent":1,"use":1,"utility":1,"valves":1,"variety":1,"venipuncture":1,"vet":1,"vinyl":1,"vriexsd":1,"water":1,"well":1,"whistle":1,"wilderness":1,"windlass":1,"wipes":1,"without":1,"working":1,"xtrm":1,"zippered":1}\t{"first":142,"aid":139,"kit":131,"camping":58,"emergency":56,"home":55,"car":54,"piece":39,"travel":39,"survival":37,"office":35,"hiking":33,"outdoor":33,"bag":28,"trauma":25,"medical":24,"kits":23,"sports":23,"supplies":22,"hunting":21,"school":19,"molle":18,"pieces":17,"case":13,"pcs":13,"osha":12,"ideal":11,"ifak":11,"purpose":11,"waterproof":11,"compact":10,"emt":10,"johnson":10,"system":10,"care":9,"compartments":9,"emergencies":9,"gear":9,"get":9,"pouch":9,"prepared":9,"smart":9,"tactical":9,"ansi":8,"boat":8,"protect":8,"boating":7,"business":7,"clean":7,"cuts":7,"fsa":7,"hsa":7,"minor":7,"mountable":7,"premium":7,"scrapes":7,"treat":7,"wall":7,"workplace":7,"backpacking":6,"earthquake":6,"essential":6,"essentials":6,"hard":6,"portable":6,"upgrade":6,"adventures":5,"compatible":5,"comprehensive":5,"fully":5,"go":5,"items":5,"outdoors":5,"reflective":5,"set":5,"traveling":5,"blanket":4,"cars":4,"combat":4,"compliant":4,"cycling":4,"ems":4,"equipment":4,"everlit":4,"exceeds":4,"grade":4,"labelled":4,"military":4,"pack":4,"pc":4,"preparedness":4,"responder":4,"shoulder":4,"stocked":4,"strap":4,"tourniquet":4,"vehicle":4,"w":4,"bandage":3,"cabinet":3,"guidelines":3,"hardcase":3,"hospital":3,"includes":3,"israeli":3,"kids":3,"packed":3,"people":3,"person":3,"pockets":3,"rapid":3,"ready":3,"rescue":3,"safety":3,"scherber":3,"splint":3,"surviveware":3,"work":3,"x":3,"yiderbo":3,"zippered":3,"advanced":2,"backpack":2,"bandages":2,"bleeding":2,"blood":2,"bonus":2,"box":2,"businesses":2,"cold":2,"complete":2,"count":2,"cpr":2,"dad":2,"designed":2,"device":2,"dorm":2,"durable":2,"eligible":2,"eva":2,"every":2,"family":2,"foil":2,"g":2,"gauze":2,"gift":2,"husband":2,"injuries":2,"instant":2,"kitgo":2,"labeled":2,"medications":2,"organized":2,"perfect":2,"plastic":2,"purse":2,"respirator":2,"response":2,"rhino":2,"safe":2,"scissors":2,"shelf":2,"standards":2,"swiss":2,"trucks":2,"upgraded":2,"well":2,"wound":2,"accident":1,"activities":1,"adhesive":1,"adult":1,"adventure":1,"airway":1,"amorning":1,"approved":1,"assorted":1,"band":1,"basic":1,"battle":1,"bleedstop":1,"blingsting":1,"boats":1,"breakwater":1,"bright":1,"bug":1,"bulk":1,"burns":1,"cables":1,"camper":1,"carabiner":1,"carlebben":1,"chest":1,"choking":1,"class":1,"clotting":1,"clutch":1,"coach":1,"coleman":1,"college":1,"comes":1,"compressed":1,"contractor":1,"control":1,"cool":1,"coyote":1,"deftget":1,"deluxe":1,"detachable":1,"diaper":1,"disaster":1,"disasters":1,"dividers":1,"dry":1,"dual":1,"duty":1,"equipped":1,"etc":1,"ever":1,"exceed":1,"excursion":1,"exploring":1,"eyewash":1,"fae":1,"falcontac":1,"fao":1,"fill":1,"floating":1,"foot":1,"gasket":1,"gifts":1,"going":1,"great":1,"health":1,"heavy":1,"hurricanes":1,"included":1,"industries":1,"infant":1,"jj":1,"jumper":1,"kayaking":1,"keep":1,"kitchen":1,"latex":1,"layer":1,"le":1,"leal":1,"lightweight":1,"loved":1,"m":1,"masks":1,"med":1,"meets":1,"metal":1,"moderate":1,"multiple":1,"must":1,"nosebleeds":1,"npa":1,"objects":1,"obstructed":1,"ones":1,"padded":1,"pads":1,"paramedics":1,"pasenhome":1,"patients":1,"personal":1,"physicianscare":1,"poly":1,"pouches":1,"powder":1,"protection":1,"pumier":1,"pysanr":1,"rc":1,"refill":1,"removable":1,"removing":1,"requirements":1,"resistant":1,"roll":1,"rose":1,"science":1,"seal":1,"severe":1,"shbc":1,"shears":1,"shell":1,"simple":1,"smartcompliance":1,"sprains":1,"storms":1,"student":1,"suitable":1,"suitcase":1,"suivival":1,"supology":1,"supply":1,"tacticon":1,"taotop":1,"tape":1,"team":1,"tent":1,"thinner":1,"thriaid":1,"toddlers":1,"tools":1,"tritfit":1,"tropical":1,"tsa":1,"unique":1,"up":1,"urgent":1,"use":1,"utility":1,"v":1,"vented":1,"vriexsd":1,"water":1,"wounds":1,"xpress":1,"z":1,"zippers":1}\n',
    'medical\tfirst aid kit\t2\t{"medical":78,"first":18,"kit":16,"aid":15,"scissors":15,"pack":14,"trauma":14,"nursing":13,"gloves":11,"bag":10,"tape":10}\t{"first":142,"aid":139,"kit":131,"camping":58,"emergency":56,"home":55,"car":54,"piece":39,"travel":39,"survival":37,"office":35,"hiking":33,"outdoor":33,"bag":28,"trauma":25,"medical":24,"kits":23,"sports":23,"supplies":22,"hunting":21,"school":19,"molle":18,"pieces":17,"case":13}\n',
    'a\tb\t{"a":100,"b":90,"c":80,"d":70,"e":60}\t{"a":50,"b":45,"c":40,"d":35,"e":30}\n',
]

_default_local_node_name = 'jiwangyou'


class Processor:
    """"""
    _NULL = r'\N'
    _row_sep = '\t'

    def __init__(self):
        """"""
        # 用于判断是否在本地运行, 实际使用时替换为本地 `platform.node()` 的运行结果
        assert _default_local_node_name != 'xxx', \
            'Please use the result of `platform.node()` to set `_default_local_node_name` or `local_node_name`.'
        self._is_run_local = platform.node() == _default_local_node_name

        if self._is_run_local:
            self._src = test_data
        else:
            self._src = sys.stdin

        self._parse_args()
        # self._run()

    def _process_row(self, row) -> Union[list, list[list]]:
        """"""
        lq, rq = row[:2]
        lq_term_cnt_set_str, rq_term_cnt_set_str = row[-2:]
        lq_term_cnt_dict_pre, rq_term_cnt_dict_pre = eval(lq_term_cnt_set_str), eval(rq_term_cnt_set_str)
        lq_term_cnt_dict_ori, lq_term_cnt_dict = self._get_top_terms(lq_term_cnt_dict_pre)
        rq_term_cnt_dict_ori, rq_term_cnt_dict = self._get_top_terms(rq_term_cnt_dict_pre)
        co_term_key = lq_term_cnt_dict.keys() & rq_term_cnt_dict.keys()
        co_weights = []
        for k in co_term_key:
            co_weights.append(min(lq_term_cnt_dict[k], rq_term_cnt_dict[k]))
        sum_co_weights = sum(co_weights)
        doc_sim_l2r = sum_co_weights / sum(rq_term_cnt_dict.values())
        doc_sim_r2l = sum_co_weights / sum(lq_term_cnt_dict.values())

        ext_info = {
            'pkey': f'{lq}_{rq}',
            'doc_sim_l2r': doc_sim_l2r,
            'doc_sim_r2l': doc_sim_r2l,
            'term_dict_lq': '__'.join([f'{k}:{v}' for k, v in lq_term_cnt_dict_ori.items()]),
            'term_dict_rq': '__'.join([f'{k}:{v}' for k, v in rq_term_cnt_dict_ori.items()]),
        }
        ext_info_str = json.dumps(ext_info)

        if self._is_run_local:
            return [ext_info_str]
        else:
            return row[:-2] + [ext_info_str]

    def _get_top_terms(self, term_cnt_set_dict: dict):
        """"""
        top_terms = []
        term_cnt_set_sorted = sorted(term_cnt_set_dict.items(), key=lambda x: -x[1])
        for k, v in term_cnt_set_sorted:
            if v >= self._args.min_cnt:
                top_terms.append((k, v))
            if len(top_terms) >= self._args.max_terms:
                break

        ret = dict(top_terms)
        if self._args.no_max_norm:
            return ret, ret

        # sum_cnt = sum(ret.values())
        # avg_cnt = sum(ret.values()) / len(ret)
        # soft_sum = sum([math.exp(v) for v in ret.values()])
        max_cnt = max(ret.values())
        ret_norm = {k: v / max_cnt for k, v in ret.items()}
        return ret, ret_norm

    def _parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--multiple_row', action='store_true')  # if input one row and output multiple rows.
        parser.add_argument('--min_cnt', type=int, default=10)
        parser.add_argument('--max_terms', type=int, default=50)
        parser.add_argument('--no_max_norm', action='store_true')
        # self._parser.add_argument('--a', type=str, default='123')
        # self._parser.add_argument('--b', type=int, default=123)
        self._args = parser.parse_args(sys.argv[1:])

    def run(self):
        """"""
        for ln in self._src:
            try:
                row = ln[:-1].split(self._row_sep)
                ret = self._process_row(row)
                if ret:
                    self._print(ret)
            except:  # noqa
                logging.error(ln)

    def _print(self, ret):
        if ret == self._NULL or not ret:
            return
        if self._args.multiple_row:
            for row in ret:
                print(self._row_sep.join([str(it) for it in row]))
        else:
            print(self._row_sep.join([str(it) for it in ret]))



if __name__ == '__main__':
    """"""
    Processor().run()
