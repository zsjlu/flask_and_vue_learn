<template>
  <v-card class="mx-auto" max-width="500">
    <!-- <v-toolbar
      color="teal"
      dark
    >
      <v-app-bar-nav-icon></v-app-bar-nav-icon>

      <v-toolbar-title>Topics</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>
    </v-toolbar>-->

    <v-list>
      <v-list-group
        v-for="item in items"
        :key="item.title"
        v-model="item.active"
        :prepend-icon="item.action"
        no-action
      >
        <template v-slot:activator>
          <v-list-item-content>
            <v-list-item-title v-text="item.title"></v-list-item-title>
          </v-list-item-content>
        </template>

        <v-list-item v-for="child in item.items" :key="child.title" :to="child.to">
          <v-list-item-content>
            <v-list-item-title v-text="child.title"></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-group>
    </v-list>
  </v-card>
</template>

<script>
export default {
  name: "Nav",
  data: () => ({
    items: [
      {
        action: "mdi-ticket",
        active: true,
        items: [
          { title: "测试用例管理", to: "/testcase" },
          { title: "测试用例分组", to: "/" }
        ],
        title: "测试用例"
      },
      {
        action: "mdi-silverware-fork-knife",
        items: [{ title: "测试报告管理" }],
        title: "测试报告"
      },
      {
        action: "mdi-school",
        items: [{ title: "List Item" }],
        title: "Education"
      },
      {
        action: "mdi-run",
        items: [{ title: "List Item" }],
        title: "Family"
      },
      {
        action: "mdi-bottle-tonic-plus",
        items: [{ title: "List Item" }],
        title: "Health"
      },
      {
        action: "mdi-content-cut",
        items: [{ title: "List Item" }],
        title: "Office"
      },
      {
        action: "mdi-tag",
        items: [{ title: "List Item" }],
        title: "Promotions"
      }
    ]
  })
};
</script>

