use std::{
    env,
    fs::File,
    io::{self, Read, Write},
    path::Path
};

fn main() -> io::Result<()>
{
    let args = env::args().collect::<Vec<String>>();

    if args.len() != 3 {
        eprintln!("Usage : PACKER <input_binary> <output_binary>");
        return Ok(());
    }

    let input_path = Path::new(&args[1]);
    let output_path = Path::new(&args[2]);
    let mut input_binary = File::open(&input_path)?;
    let mut input_data = Vec::new();
    
    input_binary.read_to_end(&mut input_data)?;
    
    let mut output_binary = File::create(&output_path)?;
    output_binary.write_all(b"PACKED\n")?;
    output_binary.write_all(&input_data)?;

    println!("Packing completed successfully");
    Ok(())
}
