<template>
  <div class="container">
    <div class="col-sm-10">
      <h1>Задачи: {{ cntTasksTrue + cntTasksFalse }}</h1>
      <confirmation :message="message"
                    v-if="showConfirmation" @new_trigger="show_alert"></confirmation>
      <div>
      </div>
      <div class="d-flex flex-row justify-content-between mb-4">
        <button type="button" id="task-add" class="btn btn-success btn-sm align-left d-block"
                v-b-modal.todo-modal>
          Добавить задачу
        </button>
        <button type="button" id="task-del" class="btn btn-danger btn-sm align-left d-block"
                @click="delete_all">
          Удалить все задачи
        </button>
      </div>

      <table class="table table-dark table-stripped table-hover">
        <thead class="thead-light">
        <tr>
          <th><font color="green">Выполнено:</font></th>
          <th><font color="green">{{ cntTasksTrue }}</font></th>
          <th><font color="red">Не выполнено:</font></th>
          <th><font color="red">{{ cntTasksFalse }}</font></th>
        </tr>
        <tr>
          <th>Uid</th>
          <th>Описание</th>
          <th>Статус</th>
          <th></th>
        </tr>
        </thead>

        <tbody>
        <tr v-for="(todo,index) in todos" :key="index">
          <td class="todo-uid">{{ todo.uid }}</td>
          <td>{{ todo.description }}</td>
          <td>
            <span v-if="todo.is_completed">Выполнено</span>
            <span v-else>Не выполнено</span>
          </td>
          <td>
            <div class="btn-group" role="group">
              <button type="button"
                      class="btn btn-secondary btn-sm"
                      v-b-modal.todo-update-modal
                      @click="updateTodo(todo)">Обновить</button>
              &nbsp;
              <button type="button"
                      class="btn btn-danger btn-sm"
                      @click="deleteTodo(todo)">X</button>
            </div>
          </td>
        </tr>
        </tbody>

      </table>

      <b-modal ref="addTodoModal"
               id="todo-modal"
               title="Добавить задачу"
               hide-footer
      >
        <b-form @submit="onSubmit" @reset="onReset" class="w-100">
          <b-form-group id="form-description-group"
                        label="Описание:"
                        label-for="form-description-input">
            <b-form-input id="form-description-input"
                          type="text"
                          v-model="addTodoForm.description"
                          required
                          placeholder="Завести задачу">
            </b-form-input>
          </b-form-group>

          <b-form-group id="form-complete-group">
            <b-form-checkbox-group v-model="addTodoForm.is_completed" id="form-checks">
              <b-form-checkbox value="true">Задача выполнена?</b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>
          <b-button type="submit" variant="primary">Добавить</b-button>
          <b-button type="reset" variant="danger">Сброс</b-button>
        </b-form>
      </b-modal>
      <b-modal ref="updateTodoModal"
               id="todo-update-modal"
               title="Update"
               hide-footer>
        <b-form @submit="onUpdateSubmit" @reset="onUpdateReset" class="w-100">
          <b-form-group id="form-update-description-group"
                        label="Описание:"
                        label-for="form-update-description-input">
            <b-form-input id="form-update-description-input"
                          type="text"
                          v-model="updateTodoForm.description"
                          required>
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-update-complete-group">
            <b-form-checkbox-group v-model="updateTodoForm.is_completed" id="form-update-checks">
              <b-form-checkbox value="true">Задача выполнена?</b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>
          <b-button-group>
            <b-button type="submit" variant="primary">Обновить</b-button>
            <b-button type="reset" variant="danger">Сброс</b-button>
          </b-button-group>
        </b-form>
      </b-modal>
    </div>
  </div>
</template>

<script>

import Confirmation from './Confirmation.vue';

export default {
  name: 'Todo',
  data() {
    return {
      todos: [],
      addTodoForm: {
        description: '',
        is_completed: [],
      },
      updateTodoForm: {
        uid: 0,
        description: '',
        is_completed: [],
      },
      message: '',
      showConfirmation: false,
      cntTasksTrue: 0,
      cntTasksFalse: 0,
    };
  },
  methods: {
    getTodos() {
      this.todos = [];
      this.cntTasksTrue = 0;
      this.cntTasksFalse = 0;
      for (let i = 0; i < localStorage.length; i += 1) {
        const keyTask = localStorage.key(i);
        if (keyTask.slice(0, 5) === 'task-') {
          const parseLocalStorage = JSON.parse(localStorage.getItem(keyTask));
          this.todos.push(parseLocalStorage);
          if (parseLocalStorage.is_completed) {
            this.cntTasksTrue += 1;
          } else {
            this.cntTasksFalse += 1;
          }
        }
      }
      this.todos.sort((a, b) => a.uid - b.uid);
    },
    resetForm() {
      this.addTodoForm.description = '';
      this.addTodoForm.is_completed = [];
      this.updateTodoForm.description = '';
      this.updateTodoForm.is_completed = [];
    },
    onSubmit(event) {
      event.preventDefault();
      this.$refs.addTodoModal.hide();
      let j = 0;
      let taskKey = '';
      let maxKey = 0;
      for (let i = 0; i < localStorage.length; i += 1) {
        taskKey = localStorage.key(i);
        if (taskKey.slice(0, 5) === 'task-') {
          j = Number(taskKey.substr(5));
          if (j > maxKey) {
            maxKey = j;
          }
        }
      }
      const newKey = `task-${maxKey + 1}`;
      const requestData = {
        description: this.addTodoForm.description,
        is_completed: this.addTodoForm.is_completed.length > 0,
        uid: String(maxKey + 1),
      };
      localStorage.setItem(newKey, JSON.stringify(requestData));
      this.getTodos();
      this.message = `Задача "${requestData.description}" добавлена`;
      this.showConfirmation = true;
      this.showDismissibleAlert = true;
      this.resetForm();
    },
    onReset(event) {
      event.preventDefault();
      this.$refs.addTodoModal.hide();
      this.resetForm();
    },
    updateTodo(todo) {
      this.updateTodoForm.uid = todo.uid;
      this.updateTodoForm.description = todo.description;
      if (todo.is_completed) {
        this.updateTodoForm.is_completed = [true];
      }
    },
    onUpdateSubmit(event) {
      event.preventDefault();
      this.$refs.updateTodoModal.hide();
      const requestData = {
        description: this.updateTodoForm.description,
        is_completed: this.updateTodoForm.is_completed.length > 0,
        uid: this.updateTodoForm.uid,
      };
      localStorage.setItem(`task-${requestData.uid}`, JSON.stringify(requestData));
      this.message = 'Задача обновлена';
      this.showConfirmation = true;
      this.getTodos();
    },
    onUpdateReset(event) {
      event.preventDefault();
      this.$refs.updateTodoModal.hide();
      this.resetForm();
    },
    deleteTodo(todo) {
      localStorage.removeItem(`task-${todo.uid}`);
      this.message = 'Задача удалена из списка';
      this.getTodos();
      this.showConfirmation = true;
    },
    show_alert() {
      this.showConfirmation = !this.showConfirmation;
    },
    delete_all() {
      localStorage.clear();
      this.todos = [];
      this.cntTasksTrue = 0;
      this.cntTasksFalse = 0;
    },
  },
  components: {
    confirmation: Confirmation,
  },
  created() {
    this.getTodos();
  },
};
</script>

<style>
button#task-add#task-del {
  margin: 20px;
}
h1, td {
  text-align: left;
}
.todo-uid {
  text-align: right;
}
</style>
