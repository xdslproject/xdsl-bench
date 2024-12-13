# ruff: noqa
from xdsl.builder import Builder
from xdsl.dialects.arith import *
from xdsl.dialects.builtin import *
from xdsl.dialects.scf import *
from xdsl.ir import *
from xdsl.irdl import *
from xdsl.irdl import attr_def, result_def
from xdsl.pattern_rewriter import *


def time_database_example():
    """Time running the database example."""

    @irdl_attr_definition
    class Bag(ParametrizedAttribute):
        name = "sql.bag"
        schema: ParameterDef[Attribute]

    printer = Printer()
    # print("Bag[i32]: ")
    printer.print_attribute(Bag([i32]))

    @irdl_op_definition
    class Table(IRDLOperation):
        name = "sql.table"
        table_name = attr_def(StringAttr)
        result_bag = result_def(Bag)

    t = Table.build(
        attributes={"table_name": StringAttr("T")}, result_types=[Bag([(i32)])]
    )
    printer.print_op(t)

    module = ModuleOp([t])
    # print("\n\nModuleOp[t]: ")
    print(module)

    @irdl_op_definition
    class Selection(IRDLOperation):
        name = "sql.selection"
        input_bag = operand_def(Bag)
        filter = region_def()
        result_bag = result_def(Bag)

    @Builder.implicit_region((i32,))
    def filter(args: tuple[BlockArgument, ...]):
        # filter argument
        (arg,) = args

        add = Constant.from_int_and_width(5, 32)
        offset = Constant.from_int_and_width(5, 32)
        for _ in range(1000):
            add = Addi(add, offset)

        # const1 = Constant.from_int_and_width(5, 32)
        # const2 = Constant.from_int_and_width(5, 32)
        # add = Addi(const1, const2)
        cmp = Cmpi(arg, add, "sgt")
        # sgt stands for `signed greater than`. In xDSL, this is encoded as a predicate attribute with value 4.
        Yield(cmp)

    sel = Selection.build(result_types=[Bag([i32])], operands=[t], regions=[filter])

    # print("\nprint_op: ")
    printer.print_op(sel)

    @dataclass
    class ConstantFolding(RewritePattern):
        @op_type_rewrite_pattern
        def match_and_rewrite(self, op: Addi, rewriter: PatternRewriter):
            if isinstance(op.lhs.owner, Constant) and isinstance(
                op.rhs.owner, Constant
            ):
                lhs_data = cast(IntegerAttr[IntegerType], op.lhs.owner.value).value.data
                rhs_data = cast(IntegerAttr[IntegerType], op.rhs.owner.value).value.data
                lhs_type = cast(IntegerAttr[IntegerType], op.lhs.owner.value).type
                rewriter.replace_matched_op(
                    Constant.from_int_and_width(lhs_data + rhs_data, lhs_type)
                )

    walker = PatternRewriteWalker(
        GreedyRewritePatternApplier([ConstantFolding()]),
        walk_regions_first=True,
        apply_recursively=True,
        walk_reverse=False,
    )

    walker.rewrite_op(sel)
    # print("\n\nrewrite_op: ")
    printer.print_op(sel)

    @dataclass
    class DeadConstantElim(RewritePattern):
        @op_type_rewrite_pattern
        def match_and_rewrite(self, op: Constant, rewriter: PatternRewriter):
            if len(op.result.uses) == 0:
                rewriter.erase_matched_op()

    walker = PatternRewriteWalker(
        GreedyRewritePatternApplier([DeadConstantElim()]),
        walk_regions_first=True,
        apply_recursively=True,
        walk_reverse=False,
    )

    walker.rewrite_op(sel)
    # print("\n\nrewrite_op: ")
    printer.print_op(sel)

    @irdl_op_definition
    class SinkOp(IRDLOperation):
        name = "sql.sink"
        bag = operand_def(Bag)

    module.body.block.add_op(SinkOp.build(operands=[sel]))
    # print("\n\nmodule: ")
    printer.print(module)
