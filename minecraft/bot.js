/**
 * IDA Minecraft Companion Bot (Mineflayer)
 * Run with: node bot.js
 * Controlled via env vars + stdin JSON commands.
 */

const mineflayer = require('mineflayer');
const pathfinder = require('mineflayer-pathfinder').pathfinder;
const Movements = require('mineflayer-pathfinder').Movements;
const { GoalFollow, GoalNear } = require('mineflayer-pathfinder').goals;

const host = process.env.MC_HOST || 'localhost';
const port = parseInt(process.env.MC_PORT || '25565');
const username = process.env.MC_USERNAME || 'IDA';
const version = process.env.MC_VERSION || '1.20.1';

function send(obj) {
  console.log(JSON.stringify(obj));
}

let bot;
let currentFollow = null;

try {
  bot = mineflayer.createBot({
    host,
    port,
    username,
    version,
    hideErrors: false,
  });
} catch (err) {
  send({ event: 'error', message: err.message });
  process.exit(1);
}

bot.loadPlugin(pathfinder);

bot.once('spawn', () => {
  send({ event: 'spawn' });
  const mcData = require('minecraft-data')(bot.version);
  const defaultMove = new Movements(bot, mcData);
  bot.pathfinder.setMovements(defaultMove);
});

bot.on('chat', (username, message) => {
  if (username === bot.username) return;
  send({ event: 'chat', username, message });
});

bot.on('error', (err) => {
  send({ event: 'error', message: err.message });
});

bot.on('end', (reason) => {
  send({ event: 'end', reason: reason || 'unknown' });
  process.exit(0);
});

bot.on('kicked', (reason) => {
  send({ event: 'error', message: 'Kicked: ' + reason });
});

// Read commands from stdin
const readline = require('readline');
const rl = readline.createInterface({ input: process.stdin, terminal: false });

rl.on('line', (line) => {
  try {
    const cmd = JSON.parse(line);
    handleCommand(cmd);
  } catch (e) {
    // ignore invalid json
  }
});

function handleCommand(cmd) {
  if (!bot || !bot.entity) return;

  switch (cmd.type) {
    case 'chat':
      bot.chat(cmd.text || '');
      break;

    case 'follow':
      const player = bot.players[cmd.player];
      if (player && player.entity) {
        currentFollow = cmd.player;
        bot.pathfinder.setGoal(new GoalFollow(player.entity, 2), true);
        bot.chat(`Иду за тобой, ${cmd.player}~`);
      } else {
        bot.chat(`Не вижу игрока ${cmd.player}`);
      }
      break;

    case 'stop':
      bot.pathfinder.setGoal(null);
      currentFollow = null;
      bot.chat('Остановилась.');
      break;

    case 'come':
      // come to a specific player if given
      const target = bot.players[cmd.player || Object.keys(bot.players)[0]];
      if (target && target.entity) {
        bot.pathfinder.setGoal(new GoalNear(
          target.entity.position.x,
          target.entity.position.y,
          target.entity.position.z,
          1
        ));
      }
      break;

    default:
      break;
  }
}

// Keep following if the target moves far
setInterval(() => {
  if (currentFollow && bot.players[currentFollow] && bot.players[currentFollow].entity) {
    // pathfinder GoalFollow already handles continuous following
  }
}, 2000);

send({ event: 'starting', host, port, username });
