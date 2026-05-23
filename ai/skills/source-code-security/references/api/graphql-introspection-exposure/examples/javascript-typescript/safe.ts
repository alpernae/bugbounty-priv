export const resolvers = {
  Query: {
    invoice: async (_: unknown, args: { id: string }, ctx: Context) => {
      requireAuth(ctx);
      return ctx.db.invoice.findFirst({
        where: { id: args.id, organizationId: ctx.user.organizationId }
      });
    },
    users: async (_: unknown, _args: unknown, ctx: Context) => {
      requireRole(ctx, "admin");
      return ctx.db.user.findMany({
        where: { organizationId: ctx.user.organizationId }
      });
    }
  }
};
