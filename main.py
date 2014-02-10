#! /usr/bin/env python
#coding=utf-8
from __future__ import division
from document import createDomain
from resampling import *
from maxent import me_classify
from smote import SMOTE

domain=createDomain('kitchen')
#fullyTraining(domain.getTrains(),domain.tests)
#overSampling(domain.posTrains,domain.negTrains,domain.tests)
#underSampling_average(domain.posTrains,domain.negTrains,domain.tests)
#underSampling_combined(domain.posTrains,domain.negTrains,domain.tests)
#underSampling_combined_random(domain.posTrains,domain.negTrains,domain.tests)
#underSampling_combined_classifies(domain.posTrains,domain.negTrains,domain.tests)
underSampling_combined_random_classifies(domain.posTrains,domain.negTrains,domain.tests)
#SMOTE(domain.posTrains,domain.negTrains,domain.tests)
#overSampling_feature_combined(domain.posTrains,domain.negTrains,domain.tests)