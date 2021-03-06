import unittest

import spacy

import patterns
import quotemerger
from relationships import RelationshipHandler
from tests.TestUtilsMixin import TestUtilsMixin


class FatherDaughter1Tests (unittest.TestCase, TestUtilsMixin):

    nlp = spacy.load('fr')
    merger = quotemerger.HyphenatedNameMerger(nlp.vocab)
    nlp.add_pipe(merger.merger, first=True)

    def testFD1FindsFatherDaughterWhenBothPresent(self):
        test_case = "D’après lui, le bey de Constantine, allié â celui de Tunis, avait, dans le cours de Tannée précédente (1724) attaqué à Timproviste la tribu des Henanecha. Bou-Aziz, après s'être vu enlever par ses adversaires 8.000 têtes de bétail et une partie de ses bagages, était sur le point de se rendre, lorsque sa fille Euldjia « se fit apporter les vêtements les plus beaux « et, s’en étant vêtue, monta achevai, appela les femmes « et les filles, ses parentes ou ses amies qui montèrent « aussi à cheval ; puis, elle harangua les femmes en leur « disant : « Puisque ces hommes n’ont pas de courage « d’aller contre les Turcs qui viendront bientôt nous « violer à leurs yeux, allons nous-mêmes vendre chèrement notre vie et ne restons pas plus longtemps avec ces lâches."
        parsed_doc = self.nlp(test_case)
        relationship_set = RelationshipHandler()
        matcher = spacy.matcher.Matcher(self.nlp.vocab)
        matcher.add('FATHER_DAUGHTER_1', relationship_set.handle_fd_1, patterns.MATCHERS['FATHER_DAUGHTER_1'])
        matches = matcher(parsed_doc)
        self.assertEqual(1, len(relationship_set.relationships))
        relationship = relationship_set.relationships[0]
        self.assertEqual('Bou-Aziz', relationship.father)
        self.assertEqual('Euldjia', relationship.daughter)

    def testFD1FindsFatherDaughterWhenCommaSeparatesFilleAndName(self):
        test_case = "D’après lui, le bey de Constantine, allié â celui de Tunis, avait, dans le cours de Tannée précédente (1724) attaqué à Timproviste la tribu des Henanecha. Bou-Aziz, après s'être vu enlever par ses adversaires 8.000 têtes de bétail et une partie de ses bagages, était sur le point de se rendre, lorsque sa fille, Euldjia « se fit apporter les vêtements les plus beaux « et, s’en étant vêtue, monta achevai, appela les femmes « et les filles, ses parentes ou ses amies qui montèrent « aussi à cheval ; puis, elle harangua les femmes en leur « disant : « Puisque ces hommes n’ont pas de courage « d’aller contre les Turcs qui viendront bientôt nous « violer à leurs yeux, allons nous-mêmes vendre chèrement notre vie et ne restons pas plus longtemps avec ces lâches."
        parsed_doc = self.nlp(test_case)
        relationship_set = RelationshipHandler()
        matcher = spacy.matcher.Matcher(self.nlp.vocab)
        matcher.add('FATHER_DAUGHTER_1', relationship_set.handle_fd_1, patterns.MATCHERS['FATHER_DAUGHTER_1'])
        matches = matcher(parsed_doc)
        self.assertEqual(1, len(relationship_set.relationships))
        relationship = relationship_set.relationships[0]
        self.assertEqual('Bou-Aziz', relationship.father)
        self.assertEqual('Euldjia', relationship.daughter)

    def testFD1DoesNotFindFatherDaughterWhenFatherNotPresentInParagraph(self):
        test_case = "Il, après s'être vu enlever par ses adversaires 8.000 têtes de bétail et une partie de ses bagages, était sur le point de se rendre, lorsque sa fille, Euldjia « se fit apporter les vêtements les plus beaux « et, s’en étant vêtue, monta achevai, appela les femmes « et les filles, ses parentes ou ses amies qui montèrent « aussi à cheval ; puis, elle harangua les femmes en leur « disant : « Puisque ces hommes n’ont pas de courage « d’aller contre les Turcs qui viendront bientôt nous « violer à leurs yeux, allons nous-mêmes vendre chèrement notre vie et ne restons pas plus longtemps avec ces lâches."
        parsed_doc = self.nlp(test_case)
        relationship_set = RelationshipHandler()
        matcher = spacy.matcher.Matcher(self.nlp.vocab)
        matcher.add('FATHER_DAUGHTER_1', relationship_set.handle_fd_1, patterns.MATCHERS['FATHER_DAUGHTER_1'])
        matches = matcher(parsed_doc)
        self.assertEqual(0, len(relationship_set.relationships))

    def testFD1DoesNotFindFatherDaughterWhenCapitalizedNonNameIsPresentAfterSaFille(self):
        test_case = "Il, après s'être vu enlever par ses adversaires 8.000 têtes de bétail et une partie de ses bagages, était sur le point de se rendre, lorsque sa fille « se fit apporter les vêtements les plus beaux « et, s’en étant vêtue, monta achevai, appela les femmes « et les filles, ses parentes ou ses amies qui montèrent « aussi à cheval ; puis, elle harangua les femmes en leur « disant : « Puisque ces hommes n’ont pas de courage « d’aller contre les Turcs qui viendront bientôt nous « violer à leurs yeux, allons nous-mêmes vendre chèrement notre vie et ne restons pas plus longtemps avec ces lâches."
        parsed_doc = self.nlp(test_case)
        relationship_set = RelationshipHandler()
        matcher = spacy.matcher.Matcher(self.nlp.vocab)
        matcher.add('FATHER_DAUGHTER_1', relationship_set.handle_fd_1, patterns.MATCHERS['FATHER_DAUGHTER_1'])
        matches = matcher(parsed_doc)
        self.assertEqual(0, len(relationship_set.relationships))


class FatherDaughter4Tests (unittest.TestCase, TestUtilsMixin):

    nlp = spacy.load('fr')
    merger = quotemerger.HyphenatedNameMerger(nlp.vocab)
    nlp.add_pipe(merger.merger, first=True)

    def testFD4FindsFatherWhenPresentAndLaIsPresent(self):
        test_case = "Comme sa femme préférée, la fille de Ben-Gana, ne lui avait pas donné d’enfants, il épousa une fille des Mokrani, seigneurs de la Medjana."
        parsed_doc = self.nlp(test_case)
        relationship_set = RelationshipHandler()
        matcher = spacy.matcher.Matcher(self.nlp.vocab)
        matcher.add('FATHER_DAUGHTER_4', relationship_set.handle_fd_4, patterns.MATCHERS['FATHER_DAUGHTER_4'])
        matches = matcher(parsed_doc)
        self.assertEqual(1, len(relationship_set.relationships))
        relationship = relationship_set.relationships[0]
        self.assertEqual(relationship.father, 'Ben-Gana')
        self.assertEqual(relationship.daughter, 'unnamed daughter')

    def testFD4FindsFatherWhenPresentAndUneIsPresent(self):
        test_case = "Comme sa femme préférée, une fille de Ben-Gana, ne lui avait pas donné d’enfants, il épousa une fille des Mokrani, seigneurs de la Medjana."
        parsed_doc = self.nlp(test_case)
        relationship_set = RelationshipHandler()
        matcher = spacy.matcher.Matcher(self.nlp.vocab)
        matcher.add('FATHER_DAUGHTER_4', relationship_set.handle_fd_4, patterns.MATCHERS['FATHER_DAUGHTER_4'])
        matches = matcher(parsed_doc)
        self.assertEqual(1, len(relationship_set.relationships))
        relationship = relationship_set.relationships[0]
        self.assertEqual(relationship.father, 'Ben-Gana')
        self.assertEqual(relationship.daughter, 'unnamed daughter')

    def testFD4DoesNotFindFatherDaughterWhenFatherNotPresentInParagraph(self):
        test_case = "Comme sa femme préférée, une fille du cheik, ne lui avait pas donné d’enfants, il épousa une fille des Mokrani, seigneurs de la Medjana."
        parsed_doc = self.nlp(test_case)
        relationship_set = RelationshipHandler()
        matcher = spacy.matcher.Matcher(self.nlp.vocab)
        matcher.add('FATHER_DAUGHTER_4', relationship_set.handle_fd_4, patterns.MATCHERS['FATHER_DAUGHTER_4'])
        matches = matcher(parsed_doc)
        self.assertEqual(0, len(relationship_set.relationships))



