export const resolvers = {
  Query: {
    invoice: async (_: unknown, args: { id: string }, ctx: Context) => {
      return ctx.db.invoice.findUnique({ where: { id: args.id } });
    },
    users: async (_: unknown, _args: unknown, ctx: Context) => {
      return ctx.db.user.findMany();
    }
  }
};
