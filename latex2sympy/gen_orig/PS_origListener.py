# Generated from PS_orig.g4 by ANTLR 4.11.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .PS_origParser import PS_origParser
else:
    from PS_origParser import PS_origParser

# This class defines a complete listener for a parse tree produced by PS_origParser.
class PS_origListener(ParseTreeListener):

    # Enter a parse tree produced by PS_origParser#accent_symbol.
    def enterAccent_symbol(self, ctx:PS_origParser.Accent_symbolContext):
        pass

    # Exit a parse tree produced by PS_origParser#accent_symbol.
    def exitAccent_symbol(self, ctx:PS_origParser.Accent_symbolContext):
        pass


    # Enter a parse tree produced by PS_origParser#math.
    def enterMath(self, ctx:PS_origParser.MathContext):
        pass

    # Exit a parse tree produced by PS_origParser#math.
    def exitMath(self, ctx:PS_origParser.MathContext):
        pass


    # Enter a parse tree produced by PS_origParser#transpose.
    def enterTranspose(self, ctx:PS_origParser.TransposeContext):
        pass

    # Exit a parse tree produced by PS_origParser#transpose.
    def exitTranspose(self, ctx:PS_origParser.TransposeContext):
        pass


    # Enter a parse tree produced by PS_origParser#transform_atom.
    def enterTransform_atom(self, ctx:PS_origParser.Transform_atomContext):
        pass

    # Exit a parse tree produced by PS_origParser#transform_atom.
    def exitTransform_atom(self, ctx:PS_origParser.Transform_atomContext):
        pass


    # Enter a parse tree produced by PS_origParser#transform_scale.
    def enterTransform_scale(self, ctx:PS_origParser.Transform_scaleContext):
        pass

    # Exit a parse tree produced by PS_origParser#transform_scale.
    def exitTransform_scale(self, ctx:PS_origParser.Transform_scaleContext):
        pass


    # Enter a parse tree produced by PS_origParser#transform_swap.
    def enterTransform_swap(self, ctx:PS_origParser.Transform_swapContext):
        pass

    # Exit a parse tree produced by PS_origParser#transform_swap.
    def exitTransform_swap(self, ctx:PS_origParser.Transform_swapContext):
        pass


    # Enter a parse tree produced by PS_origParser#transform_assignment.
    def enterTransform_assignment(self, ctx:PS_origParser.Transform_assignmentContext):
        pass

    # Exit a parse tree produced by PS_origParser#transform_assignment.
    def exitTransform_assignment(self, ctx:PS_origParser.Transform_assignmentContext):
        pass


    # Enter a parse tree produced by PS_origParser#elementary_transform.
    def enterElementary_transform(self, ctx:PS_origParser.Elementary_transformContext):
        pass

    # Exit a parse tree produced by PS_origParser#elementary_transform.
    def exitElementary_transform(self, ctx:PS_origParser.Elementary_transformContext):
        pass


    # Enter a parse tree produced by PS_origParser#elementary_transforms.
    def enterElementary_transforms(self, ctx:PS_origParser.Elementary_transformsContext):
        pass

    # Exit a parse tree produced by PS_origParser#elementary_transforms.
    def exitElementary_transforms(self, ctx:PS_origParser.Elementary_transformsContext):
        pass


    # Enter a parse tree produced by PS_origParser#matrix.
    def enterMatrix(self, ctx:PS_origParser.MatrixContext):
        pass

    # Exit a parse tree produced by PS_origParser#matrix.
    def exitMatrix(self, ctx:PS_origParser.MatrixContext):
        pass


    # Enter a parse tree produced by PS_origParser#det.
    def enterDet(self, ctx:PS_origParser.DetContext):
        pass

    # Exit a parse tree produced by PS_origParser#det.
    def exitDet(self, ctx:PS_origParser.DetContext):
        pass


    # Enter a parse tree produced by PS_origParser#matrix_row.
    def enterMatrix_row(self, ctx:PS_origParser.Matrix_rowContext):
        pass

    # Exit a parse tree produced by PS_origParser#matrix_row.
    def exitMatrix_row(self, ctx:PS_origParser.Matrix_rowContext):
        pass


    # Enter a parse tree produced by PS_origParser#relation.
    def enterRelation(self, ctx:PS_origParser.RelationContext):
        pass

    # Exit a parse tree produced by PS_origParser#relation.
    def exitRelation(self, ctx:PS_origParser.RelationContext):
        pass


    # Enter a parse tree produced by PS_origParser#relation_list.
    def enterRelation_list(self, ctx:PS_origParser.Relation_listContext):
        pass

    # Exit a parse tree produced by PS_origParser#relation_list.
    def exitRelation_list(self, ctx:PS_origParser.Relation_listContext):
        pass


    # Enter a parse tree produced by PS_origParser#relation_list_content.
    def enterRelation_list_content(self, ctx:PS_origParser.Relation_list_contentContext):
        pass

    # Exit a parse tree produced by PS_origParser#relation_list_content.
    def exitRelation_list_content(self, ctx:PS_origParser.Relation_list_contentContext):
        pass


    # Enter a parse tree produced by PS_origParser#equality.
    def enterEquality(self, ctx:PS_origParser.EqualityContext):
        pass

    # Exit a parse tree produced by PS_origParser#equality.
    def exitEquality(self, ctx:PS_origParser.EqualityContext):
        pass


    # Enter a parse tree produced by PS_origParser#expr.
    def enterExpr(self, ctx:PS_origParser.ExprContext):
        pass

    # Exit a parse tree produced by PS_origParser#expr.
    def exitExpr(self, ctx:PS_origParser.ExprContext):
        pass


    # Enter a parse tree produced by PS_origParser#additive.
    def enterAdditive(self, ctx:PS_origParser.AdditiveContext):
        pass

    # Exit a parse tree produced by PS_origParser#additive.
    def exitAdditive(self, ctx:PS_origParser.AdditiveContext):
        pass


    # Enter a parse tree produced by PS_origParser#mp.
    def enterMp(self, ctx:PS_origParser.MpContext):
        pass

    # Exit a parse tree produced by PS_origParser#mp.
    def exitMp(self, ctx:PS_origParser.MpContext):
        pass


    # Enter a parse tree produced by PS_origParser#mp_nofunc.
    def enterMp_nofunc(self, ctx:PS_origParser.Mp_nofuncContext):
        pass

    # Exit a parse tree produced by PS_origParser#mp_nofunc.
    def exitMp_nofunc(self, ctx:PS_origParser.Mp_nofuncContext):
        pass


    # Enter a parse tree produced by PS_origParser#unary.
    def enterUnary(self, ctx:PS_origParser.UnaryContext):
        pass

    # Exit a parse tree produced by PS_origParser#unary.
    def exitUnary(self, ctx:PS_origParser.UnaryContext):
        pass


    # Enter a parse tree produced by PS_origParser#unary_nofunc.
    def enterUnary_nofunc(self, ctx:PS_origParser.Unary_nofuncContext):
        pass

    # Exit a parse tree produced by PS_origParser#unary_nofunc.
    def exitUnary_nofunc(self, ctx:PS_origParser.Unary_nofuncContext):
        pass


    # Enter a parse tree produced by PS_origParser#postfix.
    def enterPostfix(self, ctx:PS_origParser.PostfixContext):
        pass

    # Exit a parse tree produced by PS_origParser#postfix.
    def exitPostfix(self, ctx:PS_origParser.PostfixContext):
        pass


    # Enter a parse tree produced by PS_origParser#postfix_nofunc.
    def enterPostfix_nofunc(self, ctx:PS_origParser.Postfix_nofuncContext):
        pass

    # Exit a parse tree produced by PS_origParser#postfix_nofunc.
    def exitPostfix_nofunc(self, ctx:PS_origParser.Postfix_nofuncContext):
        pass


    # Enter a parse tree produced by PS_origParser#postfix_op.
    def enterPostfix_op(self, ctx:PS_origParser.Postfix_opContext):
        pass

    # Exit a parse tree produced by PS_origParser#postfix_op.
    def exitPostfix_op(self, ctx:PS_origParser.Postfix_opContext):
        pass


    # Enter a parse tree produced by PS_origParser#eval_at.
    def enterEval_at(self, ctx:PS_origParser.Eval_atContext):
        pass

    # Exit a parse tree produced by PS_origParser#eval_at.
    def exitEval_at(self, ctx:PS_origParser.Eval_atContext):
        pass


    # Enter a parse tree produced by PS_origParser#eval_at_sub.
    def enterEval_at_sub(self, ctx:PS_origParser.Eval_at_subContext):
        pass

    # Exit a parse tree produced by PS_origParser#eval_at_sub.
    def exitEval_at_sub(self, ctx:PS_origParser.Eval_at_subContext):
        pass


    # Enter a parse tree produced by PS_origParser#eval_at_sup.
    def enterEval_at_sup(self, ctx:PS_origParser.Eval_at_supContext):
        pass

    # Exit a parse tree produced by PS_origParser#eval_at_sup.
    def exitEval_at_sup(self, ctx:PS_origParser.Eval_at_supContext):
        pass


    # Enter a parse tree produced by PS_origParser#exp.
    def enterExp(self, ctx:PS_origParser.ExpContext):
        pass

    # Exit a parse tree produced by PS_origParser#exp.
    def exitExp(self, ctx:PS_origParser.ExpContext):
        pass


    # Enter a parse tree produced by PS_origParser#exp_nofunc.
    def enterExp_nofunc(self, ctx:PS_origParser.Exp_nofuncContext):
        pass

    # Exit a parse tree produced by PS_origParser#exp_nofunc.
    def exitExp_nofunc(self, ctx:PS_origParser.Exp_nofuncContext):
        pass


    # Enter a parse tree produced by PS_origParser#comp.
    def enterComp(self, ctx:PS_origParser.CompContext):
        pass

    # Exit a parse tree produced by PS_origParser#comp.
    def exitComp(self, ctx:PS_origParser.CompContext):
        pass


    # Enter a parse tree produced by PS_origParser#comp_nofunc.
    def enterComp_nofunc(self, ctx:PS_origParser.Comp_nofuncContext):
        pass

    # Exit a parse tree produced by PS_origParser#comp_nofunc.
    def exitComp_nofunc(self, ctx:PS_origParser.Comp_nofuncContext):
        pass


    # Enter a parse tree produced by PS_origParser#group.
    def enterGroup(self, ctx:PS_origParser.GroupContext):
        pass

    # Exit a parse tree produced by PS_origParser#group.
    def exitGroup(self, ctx:PS_origParser.GroupContext):
        pass


    # Enter a parse tree produced by PS_origParser#norm_group.
    def enterNorm_group(self, ctx:PS_origParser.Norm_groupContext):
        pass

    # Exit a parse tree produced by PS_origParser#norm_group.
    def exitNorm_group(self, ctx:PS_origParser.Norm_groupContext):
        pass


    # Enter a parse tree produced by PS_origParser#abs_group.
    def enterAbs_group(self, ctx:PS_origParser.Abs_groupContext):
        pass

    # Exit a parse tree produced by PS_origParser#abs_group.
    def exitAbs_group(self, ctx:PS_origParser.Abs_groupContext):
        pass


    # Enter a parse tree produced by PS_origParser#floor_group.
    def enterFloor_group(self, ctx:PS_origParser.Floor_groupContext):
        pass

    # Exit a parse tree produced by PS_origParser#floor_group.
    def exitFloor_group(self, ctx:PS_origParser.Floor_groupContext):
        pass


    # Enter a parse tree produced by PS_origParser#ceil_group.
    def enterCeil_group(self, ctx:PS_origParser.Ceil_groupContext):
        pass

    # Exit a parse tree produced by PS_origParser#ceil_group.
    def exitCeil_group(self, ctx:PS_origParser.Ceil_groupContext):
        pass


    # Enter a parse tree produced by PS_origParser#accent.
    def enterAccent(self, ctx:PS_origParser.AccentContext):
        pass

    # Exit a parse tree produced by PS_origParser#accent.
    def exitAccent(self, ctx:PS_origParser.AccentContext):
        pass


    # Enter a parse tree produced by PS_origParser#atom_expr_no_supexpr.
    def enterAtom_expr_no_supexpr(self, ctx:PS_origParser.Atom_expr_no_supexprContext):
        pass

    # Exit a parse tree produced by PS_origParser#atom_expr_no_supexpr.
    def exitAtom_expr_no_supexpr(self, ctx:PS_origParser.Atom_expr_no_supexprContext):
        pass


    # Enter a parse tree produced by PS_origParser#atom_expr.
    def enterAtom_expr(self, ctx:PS_origParser.Atom_exprContext):
        pass

    # Exit a parse tree produced by PS_origParser#atom_expr.
    def exitAtom_expr(self, ctx:PS_origParser.Atom_exprContext):
        pass


    # Enter a parse tree produced by PS_origParser#atom.
    def enterAtom(self, ctx:PS_origParser.AtomContext):
        pass

    # Exit a parse tree produced by PS_origParser#atom.
    def exitAtom(self, ctx:PS_origParser.AtomContext):
        pass


    # Enter a parse tree produced by PS_origParser#mathit.
    def enterMathit(self, ctx:PS_origParser.MathitContext):
        pass

    # Exit a parse tree produced by PS_origParser#mathit.
    def exitMathit(self, ctx:PS_origParser.MathitContext):
        pass


    # Enter a parse tree produced by PS_origParser#mathit_text.
    def enterMathit_text(self, ctx:PS_origParser.Mathit_textContext):
        pass

    # Exit a parse tree produced by PS_origParser#mathit_text.
    def exitMathit_text(self, ctx:PS_origParser.Mathit_textContext):
        pass


    # Enter a parse tree produced by PS_origParser#frac.
    def enterFrac(self, ctx:PS_origParser.FracContext):
        pass

    # Exit a parse tree produced by PS_origParser#frac.
    def exitFrac(self, ctx:PS_origParser.FracContext):
        pass


    # Enter a parse tree produced by PS_origParser#binom.
    def enterBinom(self, ctx:PS_origParser.BinomContext):
        pass

    # Exit a parse tree produced by PS_origParser#binom.
    def exitBinom(self, ctx:PS_origParser.BinomContext):
        pass


    # Enter a parse tree produced by PS_origParser#func_normal_functions_single_arg.
    def enterFunc_normal_functions_single_arg(self, ctx:PS_origParser.Func_normal_functions_single_argContext):
        pass

    # Exit a parse tree produced by PS_origParser#func_normal_functions_single_arg.
    def exitFunc_normal_functions_single_arg(self, ctx:PS_origParser.Func_normal_functions_single_argContext):
        pass


    # Enter a parse tree produced by PS_origParser#func_normal_functions_multi_arg.
    def enterFunc_normal_functions_multi_arg(self, ctx:PS_origParser.Func_normal_functions_multi_argContext):
        pass

    # Exit a parse tree produced by PS_origParser#func_normal_functions_multi_arg.
    def exitFunc_normal_functions_multi_arg(self, ctx:PS_origParser.Func_normal_functions_multi_argContext):
        pass


    # Enter a parse tree produced by PS_origParser#func_operator_names_single_arg.
    def enterFunc_operator_names_single_arg(self, ctx:PS_origParser.Func_operator_names_single_argContext):
        pass

    # Exit a parse tree produced by PS_origParser#func_operator_names_single_arg.
    def exitFunc_operator_names_single_arg(self, ctx:PS_origParser.Func_operator_names_single_argContext):
        pass


    # Enter a parse tree produced by PS_origParser#func_operator_names_multi_arg.
    def enterFunc_operator_names_multi_arg(self, ctx:PS_origParser.Func_operator_names_multi_argContext):
        pass

    # Exit a parse tree produced by PS_origParser#func_operator_names_multi_arg.
    def exitFunc_operator_names_multi_arg(self, ctx:PS_origParser.Func_operator_names_multi_argContext):
        pass


    # Enter a parse tree produced by PS_origParser#func_normal_single_arg.
    def enterFunc_normal_single_arg(self, ctx:PS_origParser.Func_normal_single_argContext):
        pass

    # Exit a parse tree produced by PS_origParser#func_normal_single_arg.
    def exitFunc_normal_single_arg(self, ctx:PS_origParser.Func_normal_single_argContext):
        pass


    # Enter a parse tree produced by PS_origParser#func_normal_multi_arg.
    def enterFunc_normal_multi_arg(self, ctx:PS_origParser.Func_normal_multi_argContext):
        pass

    # Exit a parse tree produced by PS_origParser#func_normal_multi_arg.
    def exitFunc_normal_multi_arg(self, ctx:PS_origParser.Func_normal_multi_argContext):
        pass


    # Enter a parse tree produced by PS_origParser#func.
    def enterFunc(self, ctx:PS_origParser.FuncContext):
        pass

    # Exit a parse tree produced by PS_origParser#func.
    def exitFunc(self, ctx:PS_origParser.FuncContext):
        pass


    # Enter a parse tree produced by PS_origParser#args.
    def enterArgs(self, ctx:PS_origParser.ArgsContext):
        pass

    # Exit a parse tree produced by PS_origParser#args.
    def exitArgs(self, ctx:PS_origParser.ArgsContext):
        pass


    # Enter a parse tree produced by PS_origParser#func_common_args.
    def enterFunc_common_args(self, ctx:PS_origParser.Func_common_argsContext):
        pass

    # Exit a parse tree produced by PS_origParser#func_common_args.
    def exitFunc_common_args(self, ctx:PS_origParser.Func_common_argsContext):
        pass


    # Enter a parse tree produced by PS_origParser#limit_sub.
    def enterLimit_sub(self, ctx:PS_origParser.Limit_subContext):
        pass

    # Exit a parse tree produced by PS_origParser#limit_sub.
    def exitLimit_sub(self, ctx:PS_origParser.Limit_subContext):
        pass


    # Enter a parse tree produced by PS_origParser#func_single_arg.
    def enterFunc_single_arg(self, ctx:PS_origParser.Func_single_argContext):
        pass

    # Exit a parse tree produced by PS_origParser#func_single_arg.
    def exitFunc_single_arg(self, ctx:PS_origParser.Func_single_argContext):
        pass


    # Enter a parse tree produced by PS_origParser#func_single_arg_noparens.
    def enterFunc_single_arg_noparens(self, ctx:PS_origParser.Func_single_arg_noparensContext):
        pass

    # Exit a parse tree produced by PS_origParser#func_single_arg_noparens.
    def exitFunc_single_arg_noparens(self, ctx:PS_origParser.Func_single_arg_noparensContext):
        pass


    # Enter a parse tree produced by PS_origParser#func_multi_arg.
    def enterFunc_multi_arg(self, ctx:PS_origParser.Func_multi_argContext):
        pass

    # Exit a parse tree produced by PS_origParser#func_multi_arg.
    def exitFunc_multi_arg(self, ctx:PS_origParser.Func_multi_argContext):
        pass


    # Enter a parse tree produced by PS_origParser#func_multi_arg_noparens.
    def enterFunc_multi_arg_noparens(self, ctx:PS_origParser.Func_multi_arg_noparensContext):
        pass

    # Exit a parse tree produced by PS_origParser#func_multi_arg_noparens.
    def exitFunc_multi_arg_noparens(self, ctx:PS_origParser.Func_multi_arg_noparensContext):
        pass


    # Enter a parse tree produced by PS_origParser#subexpr.
    def enterSubexpr(self, ctx:PS_origParser.SubexprContext):
        pass

    # Exit a parse tree produced by PS_origParser#subexpr.
    def exitSubexpr(self, ctx:PS_origParser.SubexprContext):
        pass


    # Enter a parse tree produced by PS_origParser#supexpr.
    def enterSupexpr(self, ctx:PS_origParser.SupexprContext):
        pass

    # Exit a parse tree produced by PS_origParser#supexpr.
    def exitSupexpr(self, ctx:PS_origParser.SupexprContext):
        pass


    # Enter a parse tree produced by PS_origParser#subeq.
    def enterSubeq(self, ctx:PS_origParser.SubeqContext):
        pass

    # Exit a parse tree produced by PS_origParser#subeq.
    def exitSubeq(self, ctx:PS_origParser.SubeqContext):
        pass


    # Enter a parse tree produced by PS_origParser#supeq.
    def enterSupeq(self, ctx:PS_origParser.SupeqContext):
        pass

    # Exit a parse tree produced by PS_origParser#supeq.
    def exitSupeq(self, ctx:PS_origParser.SupeqContext):
        pass



del PS_origParser