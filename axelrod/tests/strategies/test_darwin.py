"""Tests for the Darwin PD strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestDarwin(TestPlayer):

    name = "Darwin"
    player = axelrod.Darwin
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': True,
        'manipulates_source': False,
        'manipulates_state': True
    }

    def setUp(self):
        """Each test starts with a fresh genome."""
        self.player.genome = [C]
        super(TestDarwin, self).setUp()

    def test_setup(self):
        player = self.player()
        self.assertEqual(player.genome, [C])
        self.assertEqual(player.history, [])

    def test_strategy(self):
        p1 = self.player()
        p1.reset()
        self.versus_test(axelrod.Cooperator(), [(C, C)] * 5)
        self.assertEqual(p1.genome, [C] * 5)

        self.versus_test(axelrod.Defector(), [(C, D)] * 5)
        self.assertEqual(p1.genome, [D] * 4 + [C])

        # uses genome
        self.versus_test(axelrod.Cooperator(), [(C, C)] + [(D, C)] * 3 + [(C, C)] * 2)

    def test_against_geller_and_mindreader(self):
        self.assertEqual(len(self.player.genome), 1)

        self.versus_test(axelrod.GellerCooperator(), [(C, C)] * 2)
        self.assertEqual(len(self.player.genome), 2)
        #
        self.versus_test(axelrod.MindReader(), [(C, D)] * 2)
        self.assertEqual(len(self.player.genome), 2)

    def test_play(self):
        """valid_callers must contain at least one entry..."""
        self.assertTrue(len(self.player.valid_callers)>0)
        """...and should allow round_robin.play to call"""
        self.assertTrue("play" in self.player.valid_callers)
        self.play()
        self.play()

    def play(self):
        """We need this to circumvent the agent's anti-inspection measure"""
        p1 = self.player()
        p2 = axelrod.Player()
        p1.reset()
        p1.strategy(p2)
        # Genome contains only valid responses.
        self.assertEqual(p1.genome.count(C) + p1.genome.count(D), len(p1.genome))

    def test_reset_only_resets_first_move_of_genome(self):
        """Is instance correctly reset between rounds"""
        self.versus_test(axelrod.Defector(), [(C, D)] + [(D, D)] * 4)
        p1 = self.player()
        self.assertEqual(p1.genome, [D, C, C, C, D])
        p1.reset()
        self.assertEqual(p1.history, [])
        self.assertEqual(p1.genome[0], C)
        self.assertEqual(p1.genome, [C, C, C, C, D])

    def test_unique_genome(self):
        """Ensure genome remains unique class property"""
        p1 = self.player()
        p2 = self.player()
        self.assertEqual(p1.genome, [C])
        self.assertIs(p1.genome, p2.genome)
        self.versus_test(axelrod.Defector(), [(C, D)] + [(D, D)] * 4)
        self.assertEqual(p2.genome, [D, C, C, C, D])
        self.assertIs(p1.genome, p2.genome)
