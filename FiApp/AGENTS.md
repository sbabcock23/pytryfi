# AGENTS.md (FiApp)

These instructions apply to the `FiApp/` TypeScript Express + Sequelize app.

## Scope

- Keep changes local to `FiApp/` unless the user explicitly asks for repo-wide work.
- Treat this app as local/prototype-only unless the user says otherwise.
- The hardcoded local Postgres credentials in `config/config.json` and `src/config/database.ts` are intentionally tolerated for now. Do not convert them to env vars unless asked.

## App Shape

- Runtime entrypoint: `src/server.ts`.
- Sequelize instance: `src/config/database.ts`.
- Models live in `src/models/`; routes live in `src/routes/`.
- Build output goes to `dist/`; do not edit generated `dist/` files by hand.

## Commands

Run commands from `FiApp/`:

- `npm run typecheck` for the fastest validation.
- `npm run build` to emit `dist/`.
- `npm run test` currently aliases typecheck.
- `npm run db:migrate` and `npm run db:migrate:undo` for Sequelize migrations.
- `npm run dev` for local development and `npm run start` for the built app.

## Database and Migrations

- Do not run `sequelize.sync()` from imported modules. Keep schema-changing startup behavior in `src/server.ts` only.
- Keep model associations and migrations aligned. In particular, `ActivitySummary` has many `DailySteps`, so `DailySteps.activity_summary_id` must not be unique.
- Do not add random UUID remapping for existing associations. Preserve real foreign-key relationships when migrating data.
- Existing migration history is local and may be rewritten when explicitly requested, but keep the chain coherent and idempotent where practical.

## Routes and Validation

- Raw `req.body` creates/updates are known technical debt. Leave or add TODO comments when touching those paths unless the user asks to implement validation.
- When validation is requested, prefer small per-route field allowlists before adding a new validation library.
- Keep route responses simple and consistent with the existing CRUD style.

## Validation Expectations

- For route/model/script changes, run `npm run typecheck`.
- For changes that affect emitted JS or package scripts, also run `npm run build`.
- For migration changes, run `npm run db:migrate` if local Postgres on port `5433` is available; otherwise report that DB validation was not run.
- For server startup changes, smoke-test with `npm run start` after building and stop the server after it reaches the startup log.
