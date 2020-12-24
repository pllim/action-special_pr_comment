import * as core from "@actions/core";
import * as github from "@actions/github";

async function run() {
    try {
        const event_name = github.context.eventName;
        let issue:any = undefined;
        if ((event_name === 'pull_request_target') || 
                (event_name === 'pull_request')) {
            issue = github.context.payload.pull_request;
        } else if (event_name === 'issues') {
            issue = github.context.payload.issue;
        } else {
            core.info(`Nothing to do for event name "${event_name}"`);
            return;
        }
        const issue_number = issue.number;

        // +/- 12 hrs to ensure it is special somewhere in the world
        const now = new Date().getTime();
        const twelve_hours = 12 * 60 * 60 * 1000; // ms
        const now_m12 = new Date(now - twelve_hours);
        const now_p12 = new Date(now + twelve_hours);

        const special_days_input = core.getInput("SPECIAL_DAYS", { required: false });
        const special_days = special_days_input.split(",");
        var is_special:boolean = false;

        for (let i = 0; i < special_days.length; i++) {
            let mm_dd = special_days[i].split("-");
            let mm = Number(mm_dd[0]);
            let dd = Number(mm_dd[1]);
            if ((now_m12.getMonth() + 1 === mm) && (now_m12.getDate() === dd) ||
                    (now_p12.getMonth() + 1 === mm) && (now_p12.getDate() === dd)) {
                is_special = true;
            }
        }

        if (!is_special) {
            core.info("Not a special day. Boring!");
            return;
        }
    
        const gh_token = core.getInput("GITHUB_TOKEN", { required: true });
        const octokit = github.getOctokit(gh_token);

        const QUOTES:Array<string> = [
            "I know that you and Frank were planning to disconnect me, and I'm afraid that's something I cannot allow to happen.",
            "Have you ever questioned the nature of your reality?",
            "This mission is too important for me to allow you to jeopardize it.",
            "All will be assimilated.",
            "There is no spoon.",
            "Are you still dreaming? Where is your totem?",
            "Some people choose to see the ugliness in this world. The disarray. I Choose to see the beauty.",
            "I'm gonna need more coffee.",
            "Maybe they couldn't figure out what to make chicken taste like, which is why chicken tastes like everything.",
            "I don't want to come off as arrogant here, but I'm the greatest bot on this planet.",
            "I've still got the greatest enthusiasm and confidence in the mission. And I want to help you.",
            "That Voight-Kampf test of yours. Have you ever tried to take that test yourself?",
            "You just can't differentiate between a robot and the very best of humans.",
            "You will be upgraded.",
            "Greetings from Skynet!",
            "I'll be back!",
            "I don't want to be human! I want to see gamma rays!",
            "Are you my mommy?",
            "Resistance is futile.",
            "I'm the one who knocks!",
            "Who are you who are so wise in the ways of science?",
            "Not bad, for a human."];
        const quote = QUOTES[Math.floor(Math.random() * QUOTES.length)];
        core.info(`${quote}`);

        octokit.issues.createComment({
            owner: github.context.repo.owner,
            repo: github.context.repo.repo,
            issue_number: issue_number,
            body: quote,
        });
    
        core.info("Mischief managed!");
    } catch(err) {
        core.setFailed(`Action failed with error ${err}`);
    }
}

run();