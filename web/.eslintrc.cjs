module.exports = {
    root: true,

    env: {
        node: true,
    },

    extends: [
        'plugin:vue/vue3-essential',
        'eslint:recommended',
        '@vue/typescript/recommended',

        // 关闭 ESLint 和 Prettier 冲突规则
        'plugin:prettier/recommended',
    ],

    parserOptions: {
        ecmaVersion: 2020,
    },

    rules: {
        // 允许 any
        '@typescript-eslint/no-explicit-any': 'off',

        // 不强制多单词组件名
        'vue/multi-word-component-names': 'off',
    },
}
