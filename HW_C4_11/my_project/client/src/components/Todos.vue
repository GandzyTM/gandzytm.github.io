<template>
  <div class="container">
    <div class="col-sm-10">
      <h1>Задачи</h1>
      <p> Число невыполненных задач: {{n_uncompleted}} <br>
        Число выполненных задач: {{n_completed}} </p>
      <confirmation
        :message="confirmationMessage"
        :showDismissibleAlert = "showConfirmation"
        @closed="confClosed">
      </confirmation>
      <button type="button" id="task-add" class="btn btn-success btn-sm align-left d-block"
              v-b-modal.todo-modal>Добавить задачу</button>
      <table class="table table-dark table-stripped table-hover">
        <thead class="thead-light">
        <tr>
          <th>Uid</th>
          <th>Описание</th>
          <th>Выполнена?</th>
          <th></th>
        </tr>
        </thead>

        <tbody>
        <tr v-for="(todo, index) in todos" :key="index">
          <td class="todo-uid">{{ todo.uid }}</td>
          <td>{{ todo.description }}</td>
          <td>
            <span v-if="todo.is_completed">Выполнено</span>
            <span v-else>Не выполнено</span>
          </td>
          <td>
            <div class="btn-group" role="group">
              <button type="button" class="btn btn-secondary btn-sm"
                      v-b-modal.todo-update-modal
                      @click="updateTodo(todo)">
                Обновить</button>
              &nbsp;
              <button type="button"
                      class="btn btn-danger btn-sm"
                      @click="deleteTodo(todo)">
                X
              </button>
            </div>
          </td>
        </tr>
        </tbody>
      </table>

    </div>
    <b-modal ref="addTodoModal"
             id="todo-modal"
             title="Добавить задачу"
             hide-footer>
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
        on_reset: 0,
      },
      confirmationMessage: '',
      showConfirmation: false,
      n_completed: 0,
      n_uncompleted: 0,
    };
  },
  methods: {
    confClosed() {
      this.showConfirmation = false;
    },
    getTodos() {
      this.n_uncompleted = 0;
      this.n_completed = 0;
      this.todos = [];
      for (let i = 0; i < localStorage.length; i += 1) {
        const keyItem = Number(localStorage.key(i));
        // в todos добавляем задачи только с числовым ключом keyItem
        const arr = localStorage.getItem(keyItem) ? JSON.parse(localStorage.getItem(keyItem)) : [];
        if (arr.length !== 0) {
          this.todos.push(arr);
          // определение к-ва выполненных и невыполненных задач
          if (arr.is_completed) {
            this.n_completed = this.n_completed === undefined ? 0 : this.n_completed + 1;
          } else {
            this.n_uncompleted = this.n_uncompleted === undefined ? 0 : this.n_uncompleted + 1;
          }
        }
      }
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
      //  новый ИД равен длине массива или максимальному ключу задачи, увеличенному на единицу
      let newID = localStorage.length;
      for (let i = 0; i < localStorage.length; i += 1) {
        const keyItem = Number(localStorage.key(i));
        newID = (keyItem && newID <= keyItem) ? keyItem + 1 : newID;
      }
      const addOdj = {
        uid: newID,
        description: this.addTodoForm.description,
        is_completed: this.addTodoForm.is_completed.length > 0,
      };
      localStorage.setItem(newID, JSON.stringify(addOdj));
      this.getTodos();
      this.confirmationMessage = `Задача "${this.addTodoForm.description}" добавлена`;
      this.showConfirmation = true;
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
      this.updateTodoForm.is_completed = todo.is_completed;
      if (todo.is_completed) {
        this.updateTodoForm.is_completed = [true];
        this.showConfirmation = true;
      }
      this.showConfirmation = true;
    },
    onUpdateSubmit(event) {
      event.preventDefault();
      this.$refs.updateTodoModal.hide();
      this.confirmationMessage = '';
      const updOdj = {
        uid: this.updateTodoForm.uid,
        description: this.updateTodoForm.description,
        is_completed: this.updateTodoForm.is_completed.length > 0,
      };
      if (localStorage.getItem(updOdj.uid) === null) {
        alert('Запись была удалена другим пользователем'); // eslint-disable-line no-alert
        this.showConfirmation = true;
        this.confirmationMessage = 'Обновляемая запись была удалена другим пользователем';
      } else {
        localStorage.setItem(updOdj.uid, JSON.stringify(updOdj));
        if (this.updateTodoForm.on_reset === 1) {
          this.confirmationMessage += `${this.updateTodoForm.description}`;
          this.showConfirmation = true;
        } else if (updOdj.is_completed) {
          this.confirmationMessage = `Задача "${updOdj.description}" выполнена`;
          this.showConfirmation = true;
        } else {
          this.confirmationMessage = `Задача  "${updOdj.description}" обновлена`;
          this.showConfirmation = true;
        }
        this.showConfirmation = true;
      }
      this.showConfirmation = true;
      this.getTodos();
    },
    onUpdateReset(event) {
      event.preventDefault();
      this.$refs.addTodoModal.hide();
      this.updateTodoForm.on_reset = 1;
      const modife = this.updateTodoForm.description;
      this.resetForm();
      this.confirmationMessage = `Задача ${modife} заменена на ${this.updateTodoForm.description}`;
      this.showConfirmation = true;
    },
    deleteTodo(todo) {
      this.confirmationMessage = `Задача "${todo.description}" удалена из списка`;
      this.showConfirmation = true;
      localStorage.removeItem(todo.uid);
      this.getTodos();
    },
  },
  components: {
    confirmation: Confirmation,
  },
  created() {
    this.getTodos();
    // если нет сообщения,то не выводим аллерт
    this.showConfirmation = false;
  },
};
</script>

<style>
button#task-add {
  margin-top: 20px;
  margin-bottom: 20px;
}
h1, td {
  text-align: left;
}
.todo-uid {
  text-align: right;
}
</style>
