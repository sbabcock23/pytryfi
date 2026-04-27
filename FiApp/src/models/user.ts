import {
  Table,
  Column,
  Model,
  PrimaryKey,
  HasMany,
  Index,
} from "sequelize-typescript";
import { Pet } from "./pet";

@Table({ tableName: "Users" })
export class User extends Model<User> {
  @PrimaryKey
  @Column
  id!: string;

  @Index
  @Column
  email!: string;

  @Column
  first_name!: string;

  @Column
  last_name!: string;

  @Column
  phone_number?: string;

  @Column
  fi_news_notifications_enabled!: boolean;

  @HasMany(() => Pet)
  pets!: Pet[];
}
