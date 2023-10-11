<template>
  <div class="about">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">CAL</h1>
      </div>
    </div>

    <section class="section">
      <div class="columns">
        <p class="column has-text-right">
          <span>VM Name</span>
        </p>
        <p class="column">
          <span>CPU (vCPU)</span>
        </p>
        <p class="column">
          <span>Memory (GB)</span>
        </p>
        <p class="column">
          <span>Disk (GB)</span>
        </p>
        <p class="column">
          <span>Package</span>
        </p>
        <p class="column">
          <span>Add on CPU</span>
        </p>
        <p class="column">
          <span>Add on RAM</span>
        </p>
        <p class="column">
          <span>Add on Disk</span>
        </p>
        <p class="column"></p>
      </div>
      <div v-for="(p, index) in packages" v-bind:key="index">
        <div class="columns">
          <p class="column">
            <input
              v-bind:value="index + 1"
              type="number"
              class="input has-text-right"
              disabled
            />
          </p>
          <p class="column">
            <input
              v-model="p.cpu"
              type="number"
              class="input"
              v-on:change="CalPackages()"
            />
          </p>
          <p class="column">
            <input
              v-model="p.memory"
              type="number"
              class="input"
              v-on:change="CalPackages()"
            />
          </p>
          <p class="column">
            <input
              v-model="p.disk"
              type="number"
              class="input"
              v-on:change="CalPackages()"
            />
          </p>
          <p class="column">
            <input v-model="p.package" type="text" class="input" disabled />
          </p>
          <p class="column">
            <input v-model="p.addCpu" type="text" class="input" disabled />
          </p>
          <p class="column">
            <input v-model="p.addRam" type="text" class="input" disabled />
          </p>
          <p class="column">
            <input v-model="p.addDisk" type="text" class="input" disabled />
          </p>
          <p class="column">
            <button class="button is-danger mr-2" @click="DeletePackage(index)">
              Delete
            </button>
          </p>
        </div>
      </div>
      <hr />
      <div class="columns">
        <p class="column is-vcentered">
          <span>Total</span>
        </p>
        <p class="column">
          <input v-model="total.cpu" type="number" class="input" disabled />
        </p>
        <p class="column">
          <input v-model="total.memory" type="number" class="input" disabled />
        </p>
        <p class="column">
          <input v-model="total.disk" type="number" class="input" disabled />
        </p>
        <div class="column has-text-right is-vcentered">
          <span>Total Add On</span>
        </div>
        <p class="column">
          <input v-model="total.addCpu" type="number" class="input" disabled />
        </p>
        <p class="column">
          <input v-model="total.addRam" type="number" class="input" disabled />
        </p>
        <p class="column">
          <input v-model="total.addDisk" type="number" class="input" disabled />
        </p>
        <p class="column"></p>
      </div>
      <div class="mt-5">
        <button class="button is-primary mr-2" @click="AddPackage()">
          Add
        </button>
      </div>

      <div class="columns" v-for="(key, index) in RANK" v-bind:key="index">
        <div class="column is-half is-offset-3">
          <div class="columns">
            <div class="column"></div>
            <div class="column">
              <input
                type="text"
                class="input has-text-right"
                v-bind:value="RANK[key]"
                disabled
              />
            </div>
            <div class="column">
              <input
                type="number"
                v-bind:value="total[key]"
                class="input"
                disabled
              />
            </div>
            <div class="column"></div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  data() {
    return {
      RANK: {
        BRONZE: "BRONZE",
        SILVER: "SILVER",
        GOLD: "GOLD",
        PLATINUM: "PLATINUM",
        NOPACKAGE: "NOPACKAGE",
      },
      packages: [
        {
          cpu: 0,
          memory: 0,
          disk: 0,
          package: "NOPACKAGE",
          addCpu: 0,
          addRam: 0,
          addDisk: 0,
        },
      ],
      total: {
        cpu: 0,
        memory: 0,
        disk: 0,
        addCpu: 0,
        addRam: 0,
        addDisk: 0,
        PLATINUM: 0,
        GOLD: 0,
        SILVER: 0,
        BRONZE: 0,
        NOPACKAGE: 0,
      },
    };
  },
  mounted() {
    document.title = "About | StudyNet";
  },
  methods: {
    AddPackage() {
      this.packages.push({
        cpu: 0,
        memory: 0,
        disk: 0,
        package: "NOPACKAGE",
        addCpu: 0,
        addRam: 0,
        addDisk: 0,
      });
    },
    DeletePackage(index) {
      if (this.packages.length > 1) {
        this.packages.splice(index, 1);
      }
      this.CalPackages();
    },
    CalPackages() {
      console.log(this.packages);
      this.packages.forEach((item) => {
        this.CalRank(item);
        this.CalAddOn(item);
        this.SetNotMinus(item);
      });
      this.CalTotal(this.packages);
    },
    CalRank(p) {
      if (p.cpu >= 4 && p.memory >= 8 && p.disk >= 500) {
        p.package = this.RANK.PLATINUM;
      } else if (p.cpu >= 2 && p.memory >= 4 && p.disk >= 300) {
        p.package = this.RANK.GOLD;
      } else if (p.cpu >= 1 && p.memory >= 4 && p.disk >= 150) {
        p.package = this.RANK.SILVER;
      } else if (p.cpu >= 1 && p.memory >= 2 && p.disk >= 50) {
        p.package = this.RANK.BRONZE;
      }
    },
    CalAddOn(p) {
      switch (p.package) {
        case this.RANK.PLATINUM:
          p.addCpu = p.cpu - 4;
          p.addRam = p.memory - 8;
          p.addDisk = p.disk - 500;
          break;
        case this.RANK.GOLD:
          p.addCpu = p.cpu - 2;
          p.addRam = p.memory - 4;
          p.addDisk = p.disk - 300;
          break;
        case this.RANK.SILVER:
          p.addCpu = p.cpu - 1;
          p.addRam = p.memory - 4;
          p.addDisk = p.disk - 150;
          break;
        case this.RANK.BRONZE:
          p.addCpu = p.cpu - 1;
          p.addRam = p.memory - 2;
          p.addDisk = p.disk - 50;
          break;
        default:
          p.addCpu = 0;
          p.addRam = 0;
          p.addDisk = 0;
      }
    },
    SetNotMinus(p) {
      p.addCpu = p.addCpu < 0 ? 0 : p.addCpu;
      p.addRam = p.addRam < 0 ? 0 : p.addRam;
      p.addDisk = p.addDisk < 0 ? 0 : p.addDisk;
    },
    CalTotal(allp) {
      this.ResetTotal();
      allp.forEach((p) => {
        this.total.cpu += p.cpu;
        this.total.memory += p.memory;
        this.total.disk += p.disk;
        this.total.addCpu += p.addCpu;
        this.total.addRam += p.addRam;
        this.total.addDisk += p.addDisk;
        switch (p.package) {
          case this.RANK.PLATINUM:
            this.total.PLATINUM++;
            break;
          case this.RANK.GOLD:
            this.total.GOLD++;
            break;
          case this.RANK.SILVER:
            this.total.SILVER++;
            break;
          case this.RANK.BRONZE:
            this.total.BRONZE++;
            break;
          case this.RANK.NOPACKAGE:
            this.total.NOPACKAGE++;
            break;
          default:
        }
      });
    },
    ResetTotal() {
      this.total = {
        cpu: 0,
        memory: 0,
        disk: 0,
        addCpu: 0,
        addRam: 0,
        addDisk: 0,
        PLATINUM: 0,
        GOLD: 0,
        SILVER: 0,
        BRONZE: 0,
      };
    },
  },
};
</script>