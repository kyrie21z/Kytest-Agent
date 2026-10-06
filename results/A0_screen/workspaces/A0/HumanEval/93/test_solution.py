import pytest
from solution import encode


class TestEncodeBasic:
    """Test basic functionality of the encode function."""

    def test_simple_lowercase(self):
        assert encode('test') == 'TGST'

    def test_simple_uppercase(self):
        assert encode('TEST') == 'tgst'

    def test_mixed_case(self):
        assert encode('This is a message') == 'tHKS KS C MGSSCGG'

    def test_single_letter_vowel_lowercase(self):
        # 'a' -> 'A' (case swap) -> 'C' (vowel change)
        assert encode('a') == 'C'

    def test_single_letter_vowel_uppercase(self):
        # 'A' -> 'a' (case swap) -> 'c' (vowel change)
        assert encode('A') == 'c'

    def test_single_consonant_lowercase(self):
        assert encode('b') == 'B'

    def test_single_consonant_uppercase(self):
        assert encode('B') == 'b'

    def test_empty_string(self):
        assert encode('') == ''


class TestEncodeVowelReplacement:
    """Test that all vowels are replaced correctly after case swap."""

    # All lowercase vowels: case swap makes them uppercase, then vowel change shifts by 2
    def test_a_replaced_with_C(self):
        assert encode('a') == 'C'

    def test_e_replaced_with_G(self):
        assert encode('e') == 'G'

    def test_i_replaced_with_K(self):
        assert encode('i') == 'K'

    def test_o_replaced_with_Q(self):
        assert encode('o') == 'Q'

    def test_u_replaced_with_W(self):
        assert encode('u') == 'W'

    # All uppercase vowels: case swap makes them lowercase, then vowel change shifts by 2
    def test_A_replaced_with_c(self):
        assert encode('A') == 'c'

    def test_E_replaced_with_g(self):
        assert encode('E') == 'g'

    def test_I_replaced_with_k(self):
        assert encode('I') == 'k'

    def test_O_replaced_with_q(self):
        assert encode('O') == 'q'

    def test_U_replaced_with_w(self):
        assert encode('U') == 'w'


class TestEncodeCaseSwapping:
    """Test that case is swapped for consonants and non-vowels."""

    def test_lowercase_to_uppercase(self):
        assert encode('bcd') == 'BCD'

    def test_uppercase_to_lowercase(self):
        assert encode('BCD') == 'bcd'

    def test_mixed_case_input(self):
        # A->a->c, b->B, C->c, d->D, E->e->g, f->F
        assert encode('AbCdEf') == 'cBcDgF'

    def test_all_vowels_lowercase(self):
        # a->A->C, e->E->G, i->I->K, o->O->Q, u->U->W
        assert encode('aeiou') == 'CGKQW'

    def test_all_vowels_uppercase(self):
        # A->a->c, E->e->g, I->i->k, O->o->q, U->u->w
        assert encode('AEIOU') == 'cgkqw'


class TestEncodeConsonantsUnchanged:
    """Test that consonants are only case-swapped, not modified otherwise."""

    def test_b(self):
        assert encode('b') == 'B'

    def test_z(self):
        assert encode('z') == 'Z'

    def test_Z(self):
        assert encode('Z') == 'z'

    def test_word_no_vowels(self):
        assert encode('rhythm') == 'RHYTHM'


class TestEncodeSpacesAndSpecialChars:
    """Test handling of spaces and special characters."""

    def test_spaces_preserved(self):
        # h->H, e->E->G, l->L, l->L, o->O->Q, space, w->W, o->O->Q, r->R, l->L, d->D
        assert encode('hello world') == 'HGLLQ WQRLD'

    def test_multiple_spaces(self):
        # a->A->C, space, space, b->B
        assert encode('a  b') == 'C  B'

    def test_leading_trailing_spaces(self):
        # space, h->H, i->I->K, space
        assert encode(' hi ') == ' HK '

    def test_special_characters_unchanged(self):
        # h->H, e->E->G, l->L, l->L, o->O->Q, !
        assert encode('hello!') == 'HGLLQ!'

    def test_numbers_unchanged(self):
        # a->A->C, b->B, c->C, 1, 2, 3
        assert encode('abc123') == 'CBC123'

    def test_punctuation_preserved(self):
        assert encode('test.') == 'TGST.'


class TestEncodeEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_long_string(self):
        result = encode('abcdefghijklmnopqrstuvwxyz')
        # Compute expected manually:
        chars = []
        for ch in 'abcdefghijklmnopqrstuvwxyz':
            if 'a' <= ch <= 'z':
                ch = ch.upper()
            elif 'A' <= ch <= 'Z':
                ch = ch.lower()
            if ch in 'AEIOU':
                ch = chr(ord(ch) + 2)
            chars.append(ch)
        expected = ''.join(chars)
        assert result == expected

    def test_alternating_case(self):
        # Trace each char:
        # A->a->c, b->B, C->c, d->D, E->e->g, f->F, G->g, h->H, I->i->k, j->J, K->k, l->L, M->m, n->N, O->o->q, p->P, Q->q, r->R, S->s, t->T, U->u->w, v->V, W->w, x->X, Y->y, z->Z
        assert encode('AbCdEfGhIjKlMnOpQrStUvWxYz') == 'cBcDgFgHkJkLmNqPqRsTwVwXyZ'

    def test_only_vowels_and_consonants(self):
        # a->A->C, e->E->G, i->I->K, o->O->Q, u->U->W, A->a->c, E->e->g, I->i->k, O->o->q, U->u->w
        assert encode('aeiouAEIOU') == 'CGKQWcgkqw'

    def test_repeated_letters(self):
        # a->A->C, a->A->C, a->A->C
        assert encode('aaa') == 'CCC'

    def test_repeated_uppercase(self):
        # A->a->c, A->a->c, A->a->c
        assert encode('AAA') == 'ccc'

    def test_word_with_internal_capital(self):
        # H->h, e->E->G, l->L, l->L, o->O->Q, W->w, o->O->Q, r->R, l->L, d->D
        assert encode('HelloWorld') == 'hGLLQwQRLD'


class TestEncodeIdempotency:
    """Test properties of the encode function."""

    def test_double_encode_not_same(self):
        """Encoding twice should produce different results since case swapping reverses."""
        original = 'test'
        first = encode(original)
        second = encode(first)
        assert first != second

    def test_consistent_results(self):
        """Same input always produces same output."""
        msg = 'Consistent Testing'
        assert encode(msg) == encode(msg)
